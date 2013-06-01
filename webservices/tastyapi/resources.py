from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authorization import Authorization
from .models import Sample, RockType

class SampleResource(ModelResource):
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

class RockTypeResource(ModelResource):
    samples = fields.ToManyField(SampleResource, "sample_set")
    class Meta:
        resource_name = "rock_type"
        queryset = RockType.objects.all()
        authorization = Authorization()
        filtering = {
                'rock_type': ALL,
                }
