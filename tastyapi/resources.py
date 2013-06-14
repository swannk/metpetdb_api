from django.db import transaction
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
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

class SampleResource(BaseResource):
    rock_type = fields.ToOneField("webservices.tastyapi.resources.RockTypeResource",
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

class RockTypeResource(BaseResource):
    samples = fields.ToManyField(SampleResource, "sample_set")
    class Meta:
        resource_name = "rock_type"
        queryset = RockType.objects.all()
        filtering = {
                'rock_type': ALL,
                }
