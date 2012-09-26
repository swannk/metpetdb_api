# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models





class MineralTypes(models.Model):
    mineral_type_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = u'mineral_types'

class Elements(models.Model):
    element_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    alternate_name = models.CharField(max_length=100, blank=True)
    symbol = models.CharField(max_length=4, unique=True)
    atomic_number = models.IntegerField()
    weight = models.FloatField(null=True, blank=True)
    order_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'elements'

class Oxides(models.Model):
    oxide_id = models.SmallIntegerField(primary_key=True)
    element = models.ForeignKey(Elements)
    oxidation_state = models.SmallIntegerField(null=True, blank=True)
    species = models.CharField(max_length=20, unique=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    cations_per_oxide = models.SmallIntegerField(null=True, blank=True)
    conversion_factor = models.FloatField()
    order_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'oxides'

class Minerals(models.Model):
    mineral_id = models.SmallIntegerField(primary_key=True)
    real_mineral = models.ForeignKey('self')
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'minerals'

class Reference(models.Model):
    reference_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'reference'

class RockType(models.Model):
    rock_type_id = models.SmallIntegerField(primary_key=True)
    rock_type = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'rock_type'

class ImageType(models.Model):
    image_type_id = models.SmallIntegerField(primary_key=True)
    image_type = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True, blank=True)
    comments = models.CharField(max_length=250, blank=True)
    class Meta:
        db_table = u'image_type'

class ImageFormat(models.Model):
    image_format_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'image_format'

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    password = models.TextField() # This field type is a guess.
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)
    institution = models.CharField(max_length=300, blank=True)
    reference_email = models.CharField(max_length=255, blank=True)
    confirmation_code = models.CharField(max_length=32, blank=True)
    enabled = models.CharField(max_length=1)
    role_id = models.SmallIntegerField(null=True, blank=True)
    contributor_code = models.CharField(max_length=32, blank=True)
    contributor_enabled = models.CharField(max_length=1, blank=True)
    professional_url = models.CharField(max_length=255, blank=True)
    research_interests = models.CharField(max_length=1024, blank=True)
    request_contributor = models.CharField(max_length=1, blank=True)
    class Meta:
        db_table = u'users'

class SubsampleType(models.Model):
    subsample_type_id = models.SmallIntegerField(primary_key=True)
    subsample_type = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'subsample_type'

class Samples(models.Model):
    sample_id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    sesar_number = models.CharField(max_length=9, blank=True)
    public_data = models.CharField(max_length=1)
    collection_date = models.DateTimeField(null=True, blank=True)
    date_precision = models.SmallIntegerField(null=True, blank=True)
    number = models.CharField(max_length=35)
    rock_type = models.ForeignKey(RockType)
    user = models.ForeignKey(Users)
    location_error = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    collector = models.CharField(max_length=50, blank=True)
    collector = models.ForeignKey(Users, null=True, blank=True)
    location_text = models.CharField(max_length=50, blank=True)
    location = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'samples'

class Subsamples(models.Model):
    subsample_id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    public_data = models.CharField(max_length=1)
    sample = models.ForeignKey(Samples)
    user = models.ForeignKey(Users)
    grid_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    subsample_type = models.ForeignKey(SubsampleType)
    class Meta:
        db_table = u'subsamples'

class Images(models.Model):
    image_id = models.BigIntegerField(primary_key=True)
    checksum = models.CharField(max_length=50)
    version = models.IntegerField()
    sample = models.ForeignKey(Samples, null=True, blank=True)
    subsample = models.ForeignKey(Subsamples, null=True, blank=True)
    image_format = models.ForeignKey(ImageFormat, null=True, blank=True)
    image_type = models.ForeignKey(ImageType)
    width = models.SmallIntegerField()
    height = models.SmallIntegerField()
    collector = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    scale = models.SmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(Users)
    public_data = models.CharField(max_length=1)
    checksum_64x64 = models.CharField(max_length=50)
    checksum_half = models.CharField(max_length=50)
    filename = models.CharField(max_length=256)
    checksum_mobile = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = u'images'

class GeographyColumns(models.Model):
    f_table_catalog = models.TextField(blank=True) # This field type is a guess.
    f_table_schema = models.TextField(blank=True) # This field type is a guess.
    f_table_name = models.TextField(blank=True) # This field type is a guess.
    f_geography_column = models.TextField(blank=True) # This field type is a guess.
    coord_dimension = models.IntegerField(null=True, blank=True)
    srid = models.IntegerField(null=True, blank=True)
    type = models.TextField(blank=True)
    class Meta:
        db_table = u'geography_columns'

class ChemicalAnalyses(models.Model):
    chemical_analysis_id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    subsample = models.ForeignKey(Subsamples)
    public_data = models.CharField(max_length=1)
    reference_x = models.FloatField(null=True, blank=True)
    reference_y = models.FloatField(null=True, blank=True)
    stage_x = models.FloatField(null=True, blank=True)
    stage_y = models.FloatField(null=True, blank=True)
    image = models.ForeignKey(Images, null=True, blank=True)
    analysis_method = models.CharField(max_length=50, blank=True)
    where_done = models.CharField(max_length=50, blank=True)
    analyst = models.CharField(max_length=50, blank=True)
    analysis_date = models.DateTimeField(null=True, blank=True)
    date_precision = models.SmallIntegerField(null=True, blank=True)
    reference = models.ForeignKey(Reference, null=True, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    mineral = models.ForeignKey(Minerals, null=True, blank=True)
    user = models.ForeignKey(Users)
    large_rock = models.CharField(max_length=1)
    total = models.FloatField(null=True, blank=True)
    spot_id = models.BigIntegerField()
    class Meta:
        db_table = u'chemical_analyses'


class ChemicalAnalysisOxides(models.Model):
    chemical_analysis = models.ForeignKey(ChemicalAnalyses)
    oxide = models.ForeignKey(Oxides)
    amount = models.FloatField()
    precision = models.FloatField(null=True, blank=True)
    precision_type = models.CharField(max_length=3, blank=True)
    measurement_unit = models.CharField(max_length=4, blank=True)
    min_amount = models.FloatField(null=True, blank=True)
    max_amount = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'chemical_analysis_oxides'

class ElementMineralTypes(models.Model):
    element = models.ForeignKey(Elements)
    mineral_type = models.ForeignKey(MineralTypes)
    class Meta:
        db_table = u'element_mineral_types'

class GeometryColumns(models.Model):
    f_table_catalog = models.CharField(max_length=256)
    f_table_schema = models.CharField(max_length=256)
    f_table_name = models.CharField(max_length=256)
    f_geometry_column = models.CharField(max_length=256)
    coord_dimension = models.IntegerField()
    srid = models.IntegerField()
    type = models.CharField(max_length=30)
    class Meta:
        db_table = u'geometry_columns'

class Georeference(models.Model):
    georef_id = models.BigIntegerField(primary_key=True)
    title = models.TextField()
    first_author = models.TextField()
    second_authors = models.TextField(blank=True)
    journal_name = models.TextField()
    full_text = models.TextField()
    reference_number = models.TextField(blank=True)
    reference_id = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'georeference'

class Grids(models.Model):
    grid_id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    subsample = models.ForeignKey(Subsamples)
    width = models.SmallIntegerField()
    height = models.SmallIntegerField()
    public_data = models.CharField(max_length=1)
    class Meta:
        db_table = u'grids'

class ImageOnGrid(models.Model):
    image_on_grid_id = models.BigIntegerField(primary_key=True)
    grid = models.ForeignKey(Grids)
    image = models.ForeignKey(Images)
    top_left_x = models.FloatField()
    top_left_y = models.FloatField()
    z_order = models.SmallIntegerField()
    opacity = models.SmallIntegerField()
    resize_ratio = models.FloatField()
    width = models.SmallIntegerField()
    height = models.SmallIntegerField()
    checksum = models.CharField(max_length=50)
    checksum_64x64 = models.CharField(max_length=50)
    checksum_half = models.CharField(max_length=50)
    locked = models.CharField(max_length=1)
    angle = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'image_on_grid'


class MetamorphicRegions(models.Model):
    metamorphic_region_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    shape = models.TextField(blank=True) # This field type is a guess.
    description = models.TextField(blank=True)
    label_location = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = u'metamorphic_regions'

class MetamorphicRegionsBkup(models.Model):
    metamorphic_region_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    shape = models.TextField(blank=True) # This field type is a guess.
    description = models.TextField(blank=True)
    label_location = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = u'metamorphic_regions_bkup'

class SampleComments(models.Model):
    comment_id = models.BigIntegerField(primary_key=True)
    sample = models.ForeignKey(Samples)
    user = models.ForeignKey(Users)
    comment_text = models.TextField()
    date_added = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sample_comments'

class SampleMetamorphicRegionsBkup(models.Model):
    sample_id = models.BigIntegerField(null=True, blank=True)
    metamorphic_region_id = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'sample_metamorphic_regions_bkup'

class SampleAliases(models.Model):
    sample_alias_id = models.BigIntegerField(primary_key=True)
    sample = models.ForeignKey(Samples, null=True, blank=True)
    alias = models.CharField(max_length=35)
    class Meta:
        db_table = u'sample_aliases'


class OxideMineralTypes(models.Model):
    oxide = models.ForeignKey(Oxides)
    mineral_type = models.ForeignKey(MineralTypes)
    class Meta:
        db_table = u'oxide_mineral_types'

class Projects(models.Model):
    project_id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    user = models.ForeignKey(Users)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    isactive = models.CharField(max_length=1, blank=True)
    class Meta:
        db_table = u'projects'

class ProjectSamples(models.Model):
    project = models.ForeignKey(Projects)
    sample = models.ForeignKey(Samples)
    class Meta:
        db_table = u'project_samples'

class ProjectMembers(models.Model):
    project = models.ForeignKey(Projects)
    user = models.ForeignKey(Users)
    class Meta:
        db_table = u'project_members'



class ProjectInvites(models.Model):
    invite_id = models.IntegerField(primary_key=True)
    project = models.ForeignKey(Projects)
    user = models.ForeignKey(Users)
    action_timestamp = models.DateTimeField()
    status = models.CharField(max_length=32, blank=True)
    class Meta:
        db_table = u'project_invites'



class Roles(models.Model):
    role_id = models.SmallIntegerField(primary_key=True)
    role_name = models.CharField(max_length=50)
    rank = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'roles'



class Regions(models.Model):
    region_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'regions'



class MetamorphicGrades(models.Model):
    metamorphic_grade_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'metamorphic_grades'

class SampleMetamorphicGrades(models.Model):
    sample = models.ForeignKey(Samples)
    metamorphic_grade = models.ForeignKey(MetamorphicGrades)
    class Meta:
        db_table = u'sample_metamorphic_grades'

class SampleMetamorphicRegions(models.Model):
    sample = models.ForeignKey(Samples)
    metamorphic_region_id = models.SmallIntegerField()
    class Meta:
        db_table = u'sample_metamorphic_regions'

class Subsamples(models.Model):
    subsample_id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    public_data = models.CharField(max_length=1)
    sample = models.ForeignKey(Samples)
    user = models.ForeignKey(Users)
    grid_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    subsample_type = models.ForeignKey(SubsampleType)
    class Meta:
        db_table = u'subsamples'

class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True)
    auth_srid = models.IntegerField(null=True, blank=True)
    srtext = models.CharField(max_length=2048, blank=True)
    proj4text = models.CharField(max_length=2048, blank=True)
    class Meta:
        db_table = u'spatial_ref_sys'





class UsersRoles(models.Model):
    user_id = models.IntegerField()
    role_id = models.SmallIntegerField()
    class Meta:
        db_table = u'users_roles'

class UploadedFiles(models.Model):
    uploaded_file_id = models.BigIntegerField(primary_key=True)
    hash = models.CharField(max_length=50)
    filename = models.CharField(max_length=255)
    time = models.DateTimeField()
    user = models.ForeignKey(Users, null=True, blank=True)
    class Meta:
        db_table = u'uploaded_files'



class XrayImage(models.Model):
    image = models.ForeignKey(Images, primary_key=True)
    element = models.CharField(max_length=256, blank=True)
    dwelltime = models.SmallIntegerField(null=True, blank=True)
    current = models.SmallIntegerField(null=True, blank=True)
    voltage = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'xray_image'

class SampleReference(models.Model):
    sample = models.ForeignKey(Samples)
    reference = models.ForeignKey(Reference)
    class Meta:
        db_table = u'sample_reference'

class SampleRegions(models.Model):
    sample = models.ForeignKey(Samples)
    region = models.ForeignKey(Regions)
    class Meta:
        db_table = u'sample_regions'

class ChemicalAnalysisElements(models.Model):
    chemical_analysis = models.ForeignKey(ChemicalAnalyses)
    element = models.ForeignKey(Elements)
    amount = models.FloatField()
    precision = models.FloatField(null=True, blank=True)
    precision_type = models.CharField(max_length=3, blank=True)
    measurement_unit = models.CharField(max_length=4, blank=True)
    min_amount = models.FloatField(null=True, blank=True)
    max_amount = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'chemical_analysis_elements'

class MineralRelationships(models.Model):
    parent_mineral = models.ForeignKey(Minerals)
    child_mineral = models.ForeignKey(Minerals)
    class Meta:
        db_table = u'mineral_relationships'

class SampleMinerals(models.Model):
    mineral = models.ForeignKey(Minerals)
    sample = models.ForeignKey(Samples)
    amount = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'sample_minerals'






