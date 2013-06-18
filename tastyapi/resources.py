from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from . import models

class BaseResource(ModelResource):
    @transaction.commit_manually
    def dispatch(self, *args, **kwargs):
        # Transaction begins immediately, before we get here
        try:
            response = super(ModelResource, self).dispatch(*args, **kwargs)
            keep = (200 <= response.status_code < 400)
        except:
            transaction.rollback()
            raise
        else:
            if keep:
                transaction.commit()
            else:
                transaction.rollback()
            return response

class VersionedResource(BaseResource):
    def hydrate_version(self, bundle):
        if 'version' in bundle.data:
            bundle.data['version'] += 1
        else:
            bundle.data['version'] = 1
        return bundle

class VersionValidation(Validation):
    def __init__(self, queryset, pk_field):
        self.queryset = queryset
        self.pk_field = pk_field
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'No data.'}
        errors = {}
        if self.pk_field in bundle.data:
            try:
                previous = self.queryset.get(pk=bundle.data[self.pk_field])
            except ObjectDoesNotExist:
                previous = None
        else:
            previous = None
        if previous is None:
            if request is not None and request.method == 'PUT':
                return {'__all__': 'Cannot find previous version (use POST to create).'}
            elif 'version' in bundle.data and bundle.data['version'] != 0:
                # A version of 0 will be incremented to 1 during hydration
                return {'version': 'This should be 0 or absent.'}
        else:
            if request is not None and request.method == 'POST':
                return {'__all__': 'That object already exists (use PUT to update).'}
            elif 'version' not in bundle.data:
                return {'__all__': 'Data corrupted (version number missing).'}
            elif bundle.data['version'] != previous.version:
                return {'version': 'Edit conflict (object has changed since last GET).'}
        return {}



class SampleResource(VersionedResource):
    rock_type = fields.ToOneField("tastyapi.resources.RockTypeResource",
                                  "rock_type")
    class Meta:
        queryset = models.Sample.objects.all()
        authorization = Authorization()
        excludes = ['user', 'collector', 'location']
        filtering = {
                'version': ALL,
                'sesar_number': ALL,
                'public_data': ALL,
                'collection_date': ALL,
                'rock_type': ALL_WITH_RELATIONS,
                }
        validation = VersionValidation(queryset, 'id')

class RockTypeResource(BaseResource):
    samples = fields.ToManyField(SampleResource, "sample_set")
    class Meta:
        resource_name = "rock_type"
        queryset = models.RockType.objects.all()
        filtering = {
                'rock_type': ALL,
                }

class SubsampleTypeResource(BaseResource):
    subsamples = fields.ToManyField("tastyapi.resources.SubsampleResource",
                                 "subsample_set")
    class Meta:
        resource_name = 'subsample_type'
        queryset = models.SubsampleType.objects.all()
        filtering = {'subsample_type': ALL}

class SubsampleResource(VersionedResource):
    sample = fields.ToOneField(SampleResource, "sample")
    subsample_type = fields.ToOneField(SubsampleTypeResource, "subsample_type")
    class Meta:
        queryset = models.Subsample.objects.all()
        excludes = ['user']
        authorization = Authorization()
        filtering = {
                'public_data': ALL,
                'grid_id': ALL,
                'name': ALL,
                'subsample_type': ALL_WITH_RELATIONS,
                }
        validation = VersionValidation(queryset, 'subsample_id')


class ReferenceResource(BaseResource):
    subsamples = fields.ToManyField('tastyapi.resources.ChemicalAnalysisResource',
                                    'subsample_set')
    class Meta:
        queryset = models.Reference.objects.all()
        filtering = {'name': ALL}

class ChemicalAnalysisResource(VersionedResource):
    subsample = fields.ToOneField(SubsampleResource, "subsample")
    reference = fields.ToOneField(ReferenceResource, "reference")
    class Meta:
        resource_name = 'chemical_analysis'
        queryset = models.ChemicalAnalysis.objects.all()
        excludes = ['image', 'mineral', 'user']
        authorization = Authorization()
        filtering = {
                'subsample': ALL_WITH_RELATIONS,
                'reference': ALL_WITH_RELATIONS,
                'public_data': ALL,
                'reference_x': ALL,
                'reference_y': ALL,
                'stage_x': ALL,
                'stage_y': ALL,
                'analysis_method': ALL,
                'where_done': ALL,
                'analyst': ALL,
                'analysis_date': ALL,
                'large_rock': ALL,
                'total': ALL,
                }
        validation = VersionValidation(queryset, 'chemical_analysis_id')

