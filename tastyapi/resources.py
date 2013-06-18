from django.db import transaction
from django.core.exceptions import DoesNotExist
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from .models import Sample, RockType

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
            except DoesNotExist:
                previous = None
        else:
            previous = None
        if previous is None:
            if request is not None and request.method == 'PUT':
                return {'__all__': 'Cannot find previous version (use POST to create).'}
            elif 'version' in bundle.data and bundle.data['version'] != 0:
                # A version of 0 will be incremented to 1 during hydration
                return {'version': 'Cannot find previous version.'}
        else:
            if request is not None and request.method == 'POST':
                return {'__all__': 'That object already exists (use PUT to update).'}
            if 'version' not in bundle.data:
                return {'__all__': 'That object already exists (you must specify a version).'}
            elif bundle.data['version'] != previous.version:
                return {'version': 'Edit conflict (object has changed since last GET).'}
        return {}



class SampleResource(VersionedResource):
    rock_type = fields.ToOneField("tastyapi.resources.RockTypeResource",
                                  "rock_type")
    class Meta:
        queryset = Sample.objects.all()
        authorization = Authorization()
        excludes = ['user_id', 'collector_id', 'location']
        filtering = {
                'version': ALL,
                'sesar_number': ALL,
                'public_data': ALL,
                'collection_date': ALL,
                'rock_type': ALL_WITH_RELATIONS,
                }
        validation = VersionValidation(Sample.objects.all(), 'sample_id')

class RockTypeResource(BaseResource):
    samples = fields.ToManyField(SampleResource, "sample_set")
    class Meta:
        resource_name = "rock_type"
        queryset = RockType.objects.all()
        filtering = {
                'rock_type': ALL,
                }
