from django.http import HttpResponse
from webservices.models import *
import json
import sys
sys.stdout = sys.stderr
def index(request):
    	return HttpResponse('Hello universe!')

def samples(request):
	samples_data=[]
	samples=Samples.objects.filter(public_data='Y')
	i=0
	for sample in samples:
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
		
		sample_data["sample_id"]=sample.sample_id
		sample_data["label"]=sample_number
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

def chemical_analyses(request):
	chemical_analyses_data=[]
	chemical_analyses=ChemicalAnalyses.objects.filter(public_data='Y')
	id=0
	i=0
	for chemical_analysis in chemical_analyses:
		chemical_analysis_data={}
		chemical_analysis_large_rock=""
		chemical_analysis_mineral_name=""
		chemical_analysis_owner=""
		chemical_analysis_rock_type=""
		chemical_analysis_metamorphic_grade=[]
		chemical_analysis_method=""
		chemical_analysis_first_authors=[]
		chemical_analysis_publication_journal_names=[]
		chemical_analysis_total_weight=""
		chemical_analysis_elements=[]
		chemical_analysis_oxides=[]
		chemical_analysis_latlon=""
		
		#get lat lon from location
                sample_location_x=Samples.objects.raw('select sample_id,st_X(location) as geo from samples where sample_id='+str(chemical_analysis.subsample.sample.sample_id))[0].geo
                sample_location_y=Samples.objects.raw('select sample_id,st_Y(location) as geo from samples where sample_id='+str(chemical_analysis.subsample.sample.sample_id))[0].geo
                chemical_analysis_latlon=str(sample_location_y)+","+str(sample_location_x)

		#get chemical analysis large rock
		chemical_analysis_large_rock=chemical_analysis.large_rock
		
		#get chemical analysis mineral name
		try:
			chemical_analysis_mineral_name=chemical_analysis.mineral.name
		except Exception as e:
			print str(e)
		#get chemical analysis method
		chemical_analysis_method=chemical_analysis.analysis_method

		#get chemical analysis owner
		chemical_analysis_owner=chemical_analysis.user.name

		#get chemical analysis total weight
		chemical_analysis_total_weight=chemical_analysis.total

		#get chemical analysis oxides
		chemicalanalysisoxides=chemical_analysis.chemicalanalysisoxidesdup_set.all()
		for chemicalanalysisoxide in chemicalanalysisoxides:
			chemical_analysis_oxides.append(chemicalanalysisoxide.oxide.element.name)
		
		#get chemical analysis elements
		chemicalanalysiselements=chemical_analysis.chemicalanalysiselementsdup_set.all()
		for chemicalanalysiselement in chemicalanalysiselements:
			chemical_analysis_elements.append(chemicalanalysiselement.element.name)

		#get chemical analysis rock type
		chemical_analysis_rock_type=chemical_analysis.subsample.sample.rock_type.rock_type
		
		#get chemical analysis metamorphic grade
		samplemetamorphicgrades=chemical_analysis.subsample.sample.samplemetamorphicgradesdup_set.all()
		for samplemetamorphicgrade in samplemetamorphicgrades:
			chemical_analysis_metamorphic_grade.append(samplemetamorphicgrade.metamorphic_grade.name)
		
		#get chemical analysis references
		chemicalreferences=chemical_analysis.subsample.sample.samplereferencedup_set.all()
		for chemicalreference in chemicalreferences:
			referencenumber=chemicalreference.reference.name
			georeferences=Georeference.objects.filter(reference_number=str(referencenumber))
			for georeference in georeferences:
				chemical_analysis_first_authors.append(georeference.first_author)
				chemical_analysis_publication_journal_names.append(georeference.journal_name)
		
		chemical_analysis_data['sample_id']=chemical_analysis.subsample.sample.sample_id
		chemical_analysis_data['label']=chemical_analysis.subsample.sample.number
		chemical_analysis_data['chemical_analysis_latlon']=chemical_analysis_latlon
		chemical_analysis_data['chemical_analysis_large_rock']=chemical_analysis_large_rock
		chemical_analysis_data['chemical_analysis_mineral_name']=chemical_analysis_mineral_name
		chemical_analysis_data['chemical_analysis_method']=chemical_analysis_method
		chemical_analysis_data['chemical_analysis_owner']=chemical_analysis_owner
		chemical_analysis_data['chemical_analysis_total_weight']=chemical_analysis_total_weight
		chemical_analysis_data['chemical_analysis_oxides']=chemical_analysis_oxides
		chemical_analysis_data['chemical_analysis_elements']=chemical_analysis_elements
		chemical_analysis_data['chemical_analysis_rock_type']=chemical_analysis_rock_type
		chemical_analysis_data['chemical_analysis_metamorphic_grade']=chemical_analysis_metamorphic_grade
		chemical_analysis_data['chemical_analysis_first_authors']=chemical_analysis_first_authors
		chemical_analysis_data['chemical_analysis_publication_journal_names']=chemical_analysis_publication_journal_names
		chemical_analyses_data.append(chemical_analysis_data)

	return HttpResponse("{\"items\":"+json.dumps(chemical_analyses_data)+"}")

				
