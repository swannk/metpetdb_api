from django.contrib import admin
from . import models
from django.contrib.gis.admin import GeoModelAdmin
from django import forms

def clean_version_closure(model):
    def clean_version(self):
        try:
            prev = model.objects.select_for_update().get(pk=self.instance.pk)
        except model.DoesNotExist:
            return 0
        if self.cleaned_data['version'] == prev.version:
            return prev.version + 1
        else:
            raise forms.ValidationError("Edit conflict detected (someone"+
                                        " changed the object since you loaded"+
                                        " the page; you'll probably have to"+
                                        " start over)")
    return clean_version


class SampleAdminForm(forms.ModelForm):
    clean_version = clean_version_closure(models.Sample)
    class Meta:
        model = models.Sample

class SubsampleAdminForm(forms.ModelForm):
    clean_version = clean_version_closure(models.Subsample)
    class Meta:
        model = models.Subsample

class ChemicalAnalysisAdminForm(forms.ModelForm):
    clean_version = clean_version_closure(models.ChemicalAnalysis)
    class Meta:
        model = models.ChemicalAnalysis

class SampleAdmin(GeoModelAdmin):
    form = SampleAdminForm

class SubsampleAdmin(admin.ModelAdmin):
    form = SubsampleAdminForm

class ChemicalAnalysisAdmin(admin.ModelAdmin):
    form = ChemicalAnalysisAdminForm

admin.site.register(models.Sample, SampleAdmin)
admin.site.register(models.RockType)
admin.site.register(models.Subsample, SubsampleAdmin)
admin.site.register(models.SubsampleType)
admin.site.register(models.ChemicalAnalysis, ChemicalAnalysisAdmin)

