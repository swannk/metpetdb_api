from django.contrib import admin
from . import models
from django.contrib.gis.admin import GeoModelAdmin

admin.site.register(models.Sample, GeoModelAdmin)
admin.site.register(models.RockType)
admin.site.register(models.Subsample)
admin.site.register(models.SubsampleType)
admin.site.register(models.ChemicalAnalysis)

