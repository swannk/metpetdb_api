# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


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

    def __unicode__(self):
        return self.name
