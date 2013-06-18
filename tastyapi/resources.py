from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from .models import Sample, RockType, Subsample, SubsampleType

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
        queryset = Sample.objects.all()
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
        queryset = RockType.objects.all()
        filtering = {
                'rock_type': ALL,
                }

class SubsampleTypeResource(BaseResource):
    samples = fields.ToManyField("tastyapi.resources.SubsampleResource",
                                 "subsample_set")
    class Meta:
        queryset = SubsampleType.objects.all()
        filtering = {'subsample_type': ALL}

class SubsampleResource(VersionedResource):
    sample = fields.ToOneField(SampleResource, "sample")
    subsample_type = fields.ToOneField(SubsampleTypeResource, "subsample_type")
    class Meta:
        queryset = Subsample.objects.all()
        excludes = ['user']
        authorization = Authorization()
        filtering = {
                'public_data': ALL,
                'grid_id': ALL,
                'name': ALL,
                'subsample_type': ALL_WITH_RELATIONS,
                }
        validation = VersionValidation(queryset, 'subsample_id')

