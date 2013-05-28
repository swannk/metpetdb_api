from django.contrib.gis.db import models

class Sample(models.Model):
    sample_id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    sesar_number = models.CharField(null=True, max_length=9)
    public_data = models.CharField(max_length=1)
    collection_date = models.DateTimeField(null=True)
    date_precision = models.SmallIntegerField(null=True)
    number = models.CharField(max_length=35)
    rock_type = models.ForeignKey('RockType', db_column='rock_type_id', on_delete=models.DO_NOTHING)
    user_id = models.SmallIntegerField()
    location_error = models.FloatField(null=True)
    country = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    collector = models.CharField(max_length=50, null=True)
    collector_id = models.IntegerField(null=True)
    location_text = models.CharField(max_length=50, null=True)
    location = models.GeometryField()
    objects = models.GeoManager()
    def __unicode__(self):
        return u"Sample #{}".format(self.sample_id)
    class Meta:
        app_label = 'webservices'
        db_table = 'samples'
        managed = False

class RockType(models.Model):
    rock_type_id = models.SmallIntegerField(primary_key=True)
    rock_type = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.rock_type
    class Meta:
        app_label = 'webservices'
        db_table = 'rock_type'
        managed = False

