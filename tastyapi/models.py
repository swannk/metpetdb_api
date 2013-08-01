from django.db.models import Model, BigIntegerField, CharField, DateTimeField, FloatField, ForeignKey, IntegerField,ManyToManyField, SmallIntegerField, TextField, AutoField, OneToOneField
from django.db.models import BooleanField, PositiveIntegerField
from django.db.models import Field
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.gis.db.models import GeoManager, PolygonField, PointField, GeometryField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

PUBLIC_GROUP_DEFAULT_NAME = 'public_group'

USER_GROUP_DEFAULT_PREFIX = 'user_group_'

class GroupExtra(Model):
    group = OneToOneField(Group)
    group_type = CharField(max_length=10, choices=(('public', 'public'),
                                                          ('u_uid', 'user'),
                                                          ('p_pid', 'project')))
    owner = ForeignKey(User, blank=True, null=True)


class GroupAccess(Model):
    group = ForeignKey(Group)
    read_access = BooleanField()
    write_access = BooleanField()
    content_type = ForeignKey(ContentType)
    object_id = PositiveIntegerField()
    accessible_object = generic.GenericForeignKey('content_type', 'object_id')
    class Meta:
        unique_together = ('group', 'content_type', 'object_id')


def get_public_groups():
    """Get or create the public group(s) as a queryset."""
    public_groups = Group.objects.filter(groupextra__group_type='public')
    if not public_groups.exists():
        # None exist, create a new one
        new_public = Group.objects.create(name=PUBLIC_GROUP_DEFAULT_NAME)
        new_public.user.add(User.objects.all())
        GroupExtra.create(group=new_public, group_type='public')
    return public_groups


# Called after a User instance is saved:
@receiver(post_save, sender=User)
def fix_user_groups(sender, instance, created, raw, **kwargs):
    """Ensure that the user has their own group and is in the public group(s)."""
    return # TODO: Make this send email instead of fixing groups immediately
    if raw:
        # DB is in an inconsistent state; abort
        return
    if not created:
        return
    public_groups = get_public_groups()
    # Now verify the user is a member of each public group
    for group in public_groups.select_for_update():
        if group not in instance.groups:
            instance.groups.add(group)
    # Verify there is precisely one uid group for this user.
    user_groups = Group.objects.filter(groupextra__group_type='u_uid',
                                       groupextra__owner=instance)
    user_groups = user_groups.select_for_update()
    if user_groups.count() != 1:
        # There isn't, so get rid of whichever do exist and create from scratch
        user_groups.delete()
        user_group_name = USER_GROUP_DEFAULT_PREFIX + instance.username
        user_group = Group.objects.create(name=user_group_name)
        user_group.user.add(instance)
        GroupExtra.create(group=user_group, group_type='u_uid', owner=instance)


@receiver(pre_save)
def fix_public(sender, instance, raw, **kwargs):
    """Make public objects publicly accessible and private objects not."""
    if raw:
        # DB is in an inconsistent state; abort
        return
    if not hasattr(sender, 'public_data'):
        # We don't need to fix this one; abort
        return
    try:
        if sender.select_for_update().get(instance).public_data == instance.public_data:
            # Did not change, abort
            return
    except sender.DoesNotExist:
        pass
    sender_type = ContentType.objects.get_for_model(sender)
    public_groups = get_public_groups()
    query = Q(groupaccess__object_id=instance.pk,
              groupaccess__content_type=sender_type)
    groups_with_item = public_groups.filter(query)
    groups_without_item = public_groups.exclude(groups_with_item)
    if instance.public_data == 'Y':
        for group in groups_without_item.select_for_update():
            group.groupaccess.create(read_access=True, write_access=False,
                                     content_type=sender_type,
                                     object_id=instance.pk)
    else:
        for group in groups_with_item.select_for_update():
            group.groupaccess.delete(content_type=sender_type,
                                     object_id=instance.pk)


class BinaryField(Field):
    description = 'A sequence of bytes'
    def db_type(self, connection):
        return 'bytea'
    def get_prep_value(self, value):
        return bytearray(value)
    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ['iexact', 'icontains', 'istartswith', 'iendswith', 
                           'year', 'month', 'day', 'week_day', 'hour', 'minute',
                           'second', 'iregex']:
            raise TypeError('%r is not a supported lookup type.' % lookup_type)
        else:
            return super(Field, self).get_prep_lookup(lookup_type, value)

PUBLIC_DATA_CHOICES = (('Y', 'Yes'),('N', 'No'))

class ImageType(Model):
    image_type_id = SmallIntegerField(primary_key=True)
    image_type = CharField(max_length=100, unique=True)
    abbreviation = CharField(max_length=10, unique=True, blank=True)
    comments = CharField(max_length=250, blank=True)
    class Meta:
        db_table = u'image_type'
        managed = False

class Image(Model):
    id = BigIntegerField(primary_key=True, db_column='image_id')
    checksum = CharField(max_length=50)
    version = IntegerField()
    sample = ForeignKey('Sample', related_name='images', null=True, blank=True)
    subsample = ForeignKey('Subsample', null=True, blank=True)
    image_format = ForeignKey('ImageFormat', null=True, blank=True)
    image_type = ForeignKey('ImageType')
    width = SmallIntegerField()
    height = SmallIntegerField()
    collector = CharField(max_length=50, blank=True)
    description = CharField(max_length=1024, blank=True)
    scale = SmallIntegerField(null=True, blank=True)
    owner = ForeignKey('User', db_column='user_id')
    public_data = CharField(max_length=1, choices=PUBLIC_DATA_CHOICES)
    group_access = generic.GenericRelation(GroupAccess)
    checksum_64x64 = CharField(max_length=50)
    checksum_half = CharField(max_length=50)
    filename = CharField(max_length=256)
    checksum_mobile = CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = u'images'
        permissions = (('read_image', 'Can read image'),)
        
class Mineral(Model):
    mineral_id = SmallIntegerField(primary_key=True)
    real_mineral = ForeignKey('self')
    name = CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'minerals'
        
class MetamorphicGrade(Model):
    metamorphic_grade_id = SmallIntegerField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'metamorphic_grades'
        
class MetamorphicRegion(Model):
    metamorphic_region_id = BigIntegerField(primary_key=True)
    name = CharField(max_length=50, unique=True)
    shape = PolygonField(blank=True, null=True)
    description = TextField(blank=True)
    label_location = GeometryField(blank=True, null=True) # This field type is a guess.
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'metamorphic_regions'
        
class Reference(Model):
    reference_id = BigIntegerField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'reference'
        
class Region(Model):
    region_id = SmallIntegerField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'regions'
        
class RockType(Model):
    rock_type_id = SmallIntegerField(primary_key=True)
    rock_type = CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.rock_type
    class Meta:
        managed = False
        db_table = u'rock_type'
                
class Sample(Model):   
    id = BigIntegerField(primary_key=True, db_column='sample_id')
    version = IntegerField()
    sesar_number = CharField(max_length=9, blank=True)
    public_data = CharField(max_length=1, choices=PUBLIC_DATA_CHOICES)
    group_access = generic.GenericRelation(GroupAccess)
    collection_date = DateTimeField(null=True, blank=True)
    date_precision = SmallIntegerField(null=True, blank=True)
    number = CharField(max_length=35)
    rock_type = ForeignKey(RockType)
    owner = ForeignKey('User', db_column='user_id', related_name='Sample_user')
    location_error = FloatField(null=True, blank=True)
    country = CharField(max_length=100, blank=True)
    description = TextField(blank=True)
    collector_name = CharField(db_column='collector', max_length=50, blank=True)
    collector = ForeignKey('User', db_column='collector_id', # would be collector_id_id
                           null=True, blank=True)
    location_text = CharField(max_length=50, blank=True)
    location = PointField()
    metamorphic_grades = ManyToManyField(MetamorphicGrade, through='SampleMetamorphicGrade')
    metamorphic_regions = ManyToManyField(MetamorphicRegion, through='SampleMetamorphicRegion')
    minerals = ManyToManyField(Mineral, through='SampleMineral')
    references = ManyToManyField(Reference, through='SampleReference')
    regions = ManyToManyField(Region, through='SampleRegion')
    def __unicode__(self):
        return u'Sample #' + unicode(self.id)
    class Meta:
        managed = False
        db_table = u'samples'
        permissions = (('read_sample', 'Can read sample'),)
        
class SampleAlias(Model):
    sample_alias_id = BigIntegerField(primary_key=True)
    sample = ForeignKey(Sample, related_name='aliases', null=True, blank=True)
    alias = CharField(max_length=35)
    def __unicode__(self):
        return self.alias
    class Meta:
        managed = False
        db_table = u'sample_aliases'
        unique_together = (('sample', 'alias'),)
        
class SampleMetamorphicGrade(Model):
    sample_metamorphic_grade_id = AutoField(primary_key=True, db_column='sample_metamorphic_grades_pk_id')
    sample = ForeignKey(Sample)
    metamorphic_grade = ForeignKey(MetamorphicGrade)
    class Meta:
        managed = False
        unique_together = (('sample', 'metamorphic_grade'),)
        db_table = u'sample_metamorphic_grades'

class SampleMetamorphicRegion(Model):
    sample_metamorphic_region_id = AutoField(primary_key=True, db_column='sample_metamorphic_regions_pk_id')
    sample = ForeignKey(Sample)
    metamorphic_region = ForeignKey(MetamorphicRegion)
    class Meta:
        managed = False
        unique_together = (('sample', 'metamorphic_region'),)
        db_table = u'sample_metamorphic_regions'
        
class SampleMineral(Model):
    sample_mineral_id = AutoField(primary_key=True, db_column='sample_minerals_pk_id')
    sample = ForeignKey(Sample)
    mineral = ForeignKey(Mineral)
    amount = CharField(max_length=30, blank=True)
    class Meta:
        managed = False
        unique_together = (('mineral', 'sample'),)
        db_table = u'sample_minerals'

class SampleReference(Model):
    sample_reference_id = AutoField(primary_key=True, db_column='sample_reference_pk_id')
    sample = ForeignKey(Sample)
    reference = ForeignKey(Reference)
    class Meta:
        managed = False
        unique_together = (('sample', 'reference'),)
        db_table = u'sample_reference'

class SampleRegion(Model):
    sample = ForeignKey(Sample)
    region = ForeignKey(Region)
    sample_region_id = AutoField(primary_key=True, db_column='sample_regions_pk_id')
    class Meta:
        managed = False
        unique_together = (('sample', 'region'),)
        db_table = u'sample_regions'





# Need to check these for validity
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

class MineralType(Model):
    mineral_type_id = SmallIntegerField(primary_key=True)
    name = CharField(max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'mineral_types'

class Element(Model):
    element_id = SmallIntegerField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    alternate_name = CharField(max_length=100, blank=True)
    symbol = CharField(max_length=4, unique=True)
    atomic_number = IntegerField()
    weight = FloatField(null=True, blank=True)
    order_id = IntegerField(null=True, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'elements'

class Oxide(Model):
    oxide_id = SmallIntegerField(primary_key=True)
    element = ForeignKey(Element)
    oxidation_state = SmallIntegerField(null=True, blank=True)
    species = CharField(max_length=20, unique=True, blank=True)
    weight = FloatField(null=True, blank=True)
    cations_per_oxide = SmallIntegerField(null=True, blank=True)
    conversion_factor = FloatField()
    order_id = IntegerField(null=True, blank=True)
    def __unicode__(self):
        return self.species
    class Meta:
        managed = False
        db_table = u'oxides'

class ImageFormat(Model):
    image_format_id = SmallIntegerField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    class Meta:
        managed = False
        db_table = u'image_format'

class User(Model):
    user_id = IntegerField(primary_key=True)
    version = IntegerField()
    name = CharField(max_length=100)
    email = CharField(max_length=255, unique=True)
    password = BinaryField()
    address = CharField(max_length=200, blank=True)
    city = CharField(max_length=50, blank=True)
    province = CharField(max_length=100, blank=True)
    country = CharField(max_length=100, blank=True)
    postal_code = CharField(max_length=15, blank=True)
    institution = CharField(max_length=300, blank=True)
    reference_email = CharField(max_length=255, blank=True)
    confirmation_code = CharField(max_length=32, blank=True)
    enabled = CharField(max_length=1)
    role_id = SmallIntegerField(null=True, blank=True)
    contributor_code = CharField(max_length=32, blank=True)
    contributor_enabled = CharField(max_length=1, blank=True)
    professional_url = CharField(max_length=255, blank=True)
    research_interests = CharField(max_length=1024, blank=True)
    request_contributor = CharField(max_length=1, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'users'

class SubsampleType(Model):
    subsample_type_id = SmallIntegerField(primary_key=True)
    subsample_type = CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.subsample_type
    class Meta:
        managed = False
        db_table = u'subsample_type'

class Subsample(Model):
    subsample_id = BigIntegerField(primary_key=True)
    version = IntegerField()
    public_data = CharField(max_length=1)
    group_access = generic.GenericRelation(GroupAccess)
    sample = ForeignKey(Sample)
    user = ForeignKey(User)
    grid_id = BigIntegerField(null=True, blank=True)
    name = CharField(max_length=100)
    subsample_type = ForeignKey(SubsampleType)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = u'subsamples'
        permissions = (('read_subsample', 'Can read subsample'),)



class GeographyColumns(Model):
    f_table_catalog = TextField(blank=True) # This field type is a guess.
    f_table_schema = TextField(blank=True) # This field type is a guess.
    f_table_name = TextField(blank=True) # This field type is a guess.
    f_geography_column = TextField(blank=True) # This field type is a guess.
    coord_dimension = IntegerField(null=True, blank=True)
    srid = IntegerField(null=True, blank=True)
    type = TextField(blank=True)
    class Meta:
        managed = False
        db_table = u'geography_columns'

class ChemicalAnalysis(Model):
    chemical_analysis_id = BigIntegerField(primary_key=True)
    version = IntegerField()
    subsample = ForeignKey(Subsample)
    public_data = CharField(max_length=1)
    group_access = generic.GenericRelation(GroupAccess)
    reference_x = FloatField(null=True, blank=True)
    reference_y = FloatField(null=True, blank=True)
    stage_x = FloatField(null=True, blank=True)
    stage_y = FloatField(null=True, blank=True)
    image = ForeignKey(Image, null=True, blank=True)
    analysis_method = CharField(max_length=50, blank=True)
    where_done = CharField(max_length=50, blank=True)
    analyst = CharField(max_length=50, blank=True)
    analysis_date = DateTimeField(null=True, blank=True)
    date_precision = SmallIntegerField(null=True, blank=True)
    reference = ForeignKey(Reference, null=True, blank=True)
    description = CharField(max_length=1024, blank=True)
    mineral = ForeignKey(Mineral, null=True, blank=True)
    user = ForeignKey(User)
    large_rock = CharField(max_length=1)
    total = FloatField(null=True, blank=True)
    spot_id = BigIntegerField()
    def __unicode__(self):
        return u'Analysis of "{}" via {} by {}.'.format(self.subsample,
                                                        self.analysis_method,
                                                        self.analyst)
    class Meta:
        managed = False
        db_table = u'chemical_analyses'
        verbose_name_plural = 'chemical analyses'
        permissions = (('read_analysis', 'Can read analysis'),)

class ChemicalAnalysisOxide(Model):
    chemical_analysis_oxide_id = AutoField(primary_key=True, db_column='chemical_analysis_oxides_pk_id')
    chemical_analysis = ForeignKey(ChemicalAnalysis)
    oxide = ForeignKey(Oxide)
    amount = FloatField()
    precision = FloatField(null=True, blank=True)
    precision_type = CharField(max_length=3, blank=True)
    measurement_unit = CharField(max_length=4, blank=True)
    min_amount = FloatField(null=True, blank=True)
    max_amount = FloatField(null=True, blank=True)
    class Meta:
        managed = False
        unique_together = (('chemical_analysis', 'oxide'),)
        db_table = u'chemical_analysis_oxides'

class ElementMineralType(Model):
    id = AutoField(primary_key=True, db_column='element_mineral_types_pk_id')
    element = ForeignKey(Element)
    mineral_type = ForeignKey(MineralType)
    class Meta:
        managed = False
        unique_together = (('element', 'mineral_type'),)
        db_table = u'element_mineral_types'

class GeometryColumns(Model):
    id = AutoField(primary_key=True, db_column='geometry_columns_pk_id')
    f_table_catalog = CharField(max_length=256)
    f_table_schema = CharField(max_length=256)
    f_table_name = CharField(max_length=256)
    f_geometry_column = CharField(max_length=256)
    coord_dimension = IntegerField()
    srid = IntegerField()
    type = CharField(max_length=30)
    class Meta:
        managed = False
        unique_together = (('f_table_catalog', 'f_table_schema', 'f_table_name', 'f_geometry_column'),)
        db_table = u'geometry_columns'

class Georeference(Model):
    georef_id = BigIntegerField(primary_key=True)
    title = TextField()
    first_author = TextField()
    second_authors = TextField(blank=True)
    journal_name = TextField()
    full_text = TextField()
    reference_number = TextField(blank=True)
    reference_id = BigIntegerField(null=True, blank=True)
    journal_name_2 = TextField(blank=True)
    doi = TextField(blank=True)
    publication_year = TextField(blank=True)
    class Meta:
        managed = False
        db_table = u'georeference'

class ImageComment(Model):
    comment_id = BigIntegerField(primary_key=True)
    image = ForeignKey(Image)
    comment_text = TextField()
    version = IntegerField()
    class Meta:
        managed = False
        db_table = u'image_comments'

class Grids(Model):
    grid_id = BigIntegerField(primary_key=True)
    version = IntegerField()
    subsample = ForeignKey(Subsample)
    width = SmallIntegerField()
    height = SmallIntegerField()
    public_data = CharField(max_length=1)
    group_access = generic.GenericRelation(GroupAccess)
    class Meta:
        managed = False
        db_table = u'grids'
        permissions = (('read_grids', 'Can read grids'),)

class ImageOnGrid(Model):
    image_on_grid_id = BigIntegerField(primary_key=True)
    grid = ForeignKey(Grids)
    image = ForeignKey(Image)
    top_left_x = FloatField()
    top_left_y = FloatField()
    z_order = SmallIntegerField()
    opacity = SmallIntegerField()
    resize_ratio = FloatField()
    width = SmallIntegerField()
    height = SmallIntegerField()
    checksum = CharField(max_length=50)
    checksum_64x64 = CharField(max_length=50)
    checksum_half = CharField(max_length=50)
    locked = CharField(max_length=1)
    angle = FloatField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = u'image_on_grid'

class AdminUser(Model):
    admin_id = IntegerField(primary_key=True)
    user = ForeignKey(User)
    class Meta:
        managed = False
        db_table = u'admin_users'

class ImageReference(Model):
    image_reference_id = AutoField(primary_key=True, db_column='image_reference_pk_id')
    image = ForeignKey(Image)
    reference = ForeignKey(Reference)
    class Meta:
        managed = False
        unique_together = (('image', 'reference'),)
        db_table = u'image_reference'


class SampleComment(Model):
    comment_id = BigIntegerField(primary_key=True)
    sample = ForeignKey(Sample)
    user = ForeignKey(User)
    comment_text = TextField()
    date_added = DateTimeField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = u'sample_comments'

class OxideMineralType(Model):
    oxide_mineral_id = AutoField(primary_key=True, db_column='oxide_mineral_types_pk_id')
    oxide = ForeignKey(Oxide)
    mineral_type = ForeignKey(MineralType)
    class Meta:
        managed = False
        unique_together = (('oxide', 'mineral_type'),)
        db_table = u'oxide_mineral_types'

class Project(Model):
    project_id = IntegerField(primary_key=True)
    version = IntegerField()
    user = ForeignKey(User)
    name = CharField(max_length=50)
    description = CharField(max_length=300, blank=True)
    isactive = CharField(max_length=1, blank=True)
    class Meta:
        managed = False
        unique_together = (('user', 'name'),)
        db_table = u'projects'

class ProjectSample(Model):
    project_sample_id = AutoField(primary_key=True, db_column='project_sample_pk_id')
    project = ForeignKey(Project)
    sample = ForeignKey(Sample)
    class Meta:
        managed = False
        db_table = u'project_samples'

class ProjectMembers(Model):
    project_member_id = AutoField(primary_key=True, db_column='project_members_pk_id')
    project = ForeignKey(Project)
    user = ForeignKey(User)
    class Meta:
        managed = False
        unique_together = (('project', 'user'),)
        db_table = u'project_members'

class ProjectInvite(Model):
    invite_id = IntegerField(primary_key=True)
    project = ForeignKey(Project)
    user = ForeignKey(User)
    action_timestamp = DateTimeField()
    status = CharField(max_length=32, blank=True)
    class Meta:
        managed = False
        db_table = u'project_invites'

class Role(Model):
    role_id = SmallIntegerField(primary_key=True)
    role_name = CharField(max_length=50)
    rank = SmallIntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = u'roles'

class RoleChanges(Model):
    role_changes_id = BigIntegerField(primary_key=True)
    user = ForeignKey(User,related_name='RoleChanges_user')
    sponsor = ForeignKey(User,related_name='RoleChanges_sponsor')
    request_date = DateTimeField()
    finalize_date = DateTimeField(null=True, blank=True)
    role = ForeignKey(Role)
    granted = CharField(max_length=1, blank=True)
    grant_reason = TextField(blank=True)
    request_reason = TextField(blank=True)
    class Meta:
        managed = False
        unique_together = (('user', 'granted', 'role'),)
        db_table = u'role_changes'

class Subsample(Model):
    subsample_id = BigIntegerField(primary_key=True)
    version = IntegerField()
    public_data = CharField(max_length=1)
    group_access = generic.GenericRelation(GroupAccess)
    sample = ForeignKey(Sample)
    user = ForeignKey(User)
    grid_id = BigIntegerField(null=True, blank=True)
    name = CharField(max_length=100)
    subsample_type = ForeignKey(SubsampleType)
    class Meta:
        managed = False
        db_table = u'subsamples'
        permissions = (('read_subsample', 'Can read subsample'),)

class SpatialRefSys(Model):
    srid = IntegerField(primary_key=True)
    auth_name = CharField(max_length=256, blank=True)
    auth_srid = IntegerField(null=True, blank=True)
    srtext = CharField(max_length=2048, blank=True)
    proj4text = CharField(max_length=2048, blank=True)
    class Meta:
        managed = False
        db_table = u'spatial_ref_sys'

class UserRole(Model):
    user_role_id = AutoField(primary_key=True, db_column='user_roles_pk_id')
    user = ForeignKey(User)
    role = ForeignKey(Role)
    class Meta:
        managed = False
        db_table = u'users_roles'

class UploadedFiles(Model):
    uploaded_file_id = BigIntegerField(primary_key=True)
    hash = CharField(max_length=50)
    filename = CharField(max_length=255)
    time = DateTimeField()
    user = ForeignKey(User, null=True, blank=True)
    class Meta:
        managed = False
        db_table = u'uploaded_files'

class XrayImage(Model):
    image = OneToOneField(Image, primary_key=True)
    element = CharField(max_length=256, blank=True)
    dwelltime = SmallIntegerField(null=True, blank=True)
    current = SmallIntegerField(null=True, blank=True)
    voltage = SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'xray_image'
        managed = False

class ChemicalAnalysisElement(Model):
    chemical_analysis_element_id = AutoField(primary_key=True, db_column='chemical_analysis_elements_pk_id')
    chemical_analysis = ForeignKey(ChemicalAnalysis)
    element = ForeignKey(Element)
    amount = FloatField()
    precision = FloatField(null=True, blank=True)
    precision_type = CharField(max_length=3, blank=True)
    measurement_unit = CharField(max_length=4, blank=True)
    min_amount = FloatField(null=True, blank=True)
    max_amount = FloatField(null=True, blank=True)
    class Meta:
        unique_together = (('chemical_analysis', 'element'),)
        db_table = u'chemical_analysis_elements'
        managed = False

class MineralRelationship(Model):
    mineral_relationship_id = AutoField(primary_key=True, db_column='mineral_relationships_pk_id')
    parent_mineral = ForeignKey(Mineral,related_name='MineralRelationships_parent_mineral')
    child_mineral = ForeignKey(Mineral,related_name='MineralRelationships_child_mineral')
    class Meta:
        unique_together = (('parent_mineral', 'child_mineral'),)
        db_table = u'mineral_relationships'
        managed = False
