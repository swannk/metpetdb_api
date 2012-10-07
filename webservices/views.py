from django.http import HttpResponse
from webservices.models import *
import json
def index(request):
	str1=""
	for p in Users.objects.raw('SELECT * FROM Users'):
		str1=str1+unicode(p.country)+"\n"
    	return HttpResponse(str1)

def samples(request):
	samples_data=[]
	samples=Samples.objects.filter(public_data='Y')
	id=0
	i=0
	for sample in samples:
		#if i==3:
		#	break
		#i=i+1
		#initialize the variables
		sample_data={}
		sample_latlon=""
		sample_number=""
		sample_metamorphic_regions=[]
        	sample_country=""
        	sample_owner=""
        	sample_rock_type=""
        	sample_metamorphic_grades=[]
		sample_minerals=[]
		sample_regions=[]
		sample_reference_first_authors=[]
		sample_reference_journal_names=[]
		
		#get sample metamorphic regions
		samplemetamorphicregions=sample.samplemetamorphicregionsdup_set.all()
		for samplemetamorphicregion in samplemetamorphicregions:
			sample_metamorphic_regions.append(samplemetamorphicregion.metamorphic_region.name)
		
		#get lat lon from location
		
		sample_location_x=Samples.objects.raw('select sample_id,st_X(location) as geo from samples where sample_id='+str(sample.sample_id))[0].geo
		sample_location_y=Samples.objects.raw('select sample_id,st_Y(location) as geo from samples where sample_id='+str(sample.sample_id))[0].geo
		sample_latlon=str(sample_location_y)+","+str(sample_location_x)
		
		'''
		sample_latlon=Samples.objects.raw('select sample_id,substr(ST_asText(location), 7) as geo from samples where sample_id='+str(sample.sample_id))[0].geo
		sample_latlon=sample_latlon.rstrip(')')
		sample_latlon=sample_latlon.replace(' ',',')		
		'''
		
		#get sample number
		sample_number=sample.number

		#get sample country
		sample_country=sample.country
		
		#get sample owner
		sample_owner=sample.user.name

		#get sample rock type
		sample_rock_type=sample.rock_type.rock_type

		#get sample metamorphic grades
		samplemetamorphicgrades=sample.samplemetamorphicgradesdup_set.all()
		for samplemetamorphicgrade in samplemetamorphicgrades:
			sample_metamorphic_grades.append(samplemetamorphicgrade.metamorphic_grade.name)
		
		#get sample minerals
		sampleminerals=sample.samplemineralsdup_set.all()
		for samplemineral in sampleminerals:
			sample_minerals.append(samplemineral.mineral.name)

		#get sample regions
		sampleregions=sample.sampleregionsdup_set.all()
		for sampleregion in sampleregions:
			sample_regions.append(sampleregion.region.name)

		#get sample references
		samplereferences=sample.samplereferencedup_set.all()
		for samplereference in samplereferences:
			referencenumber=samplereference.reference.name
			georeferences=Georeference.objects.filter(reference_number=str(referencenumber))
			for georeference in georeferences:
				sample_reference_first_authors.append(georeference.first_author)
				sample_reference_journal_names.append(georeference.journal_name)
		
		id=id+1
		sample_data["label"]=id
		sample_data["sample_number"]=sample_number
		sample_data["sample_metamorphic_regions"]=sample_metamorphic_regions
		sample_data["sample_country"]=sample_country
		sample_data["sample_owner"]=sample_owner
		sample_data["sample_rock_type"]=sample_rock_type
		sample_data["sample_metamorphic_grades"]=sample_metamorphic_grades
		sample_data["sample_minerals"]=sample_minerals
		sample_data["sample_regions"]=sample_regions
		sample_data["sample_reference_first_author"]=sample_reference_first_authors
		sample_data["sample_reference_journal_name"]=sample_reference_journal_names
		sample_data["sample_latlon"]=sample_latlon
		samples_data.append(sample_data)
		
	return HttpResponse("{\"items\":"+json.dumps(samples_data)+"}")
