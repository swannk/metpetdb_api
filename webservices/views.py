from django.http import HttpResponse
import json
import sys
from django.db import connection as con
from webservices.SampleQuery import *
from webservices.utility import *
from webservices.sample import SampleObject, SampleImagesObject
from webservices.subsample import SubsampleObject, SubsampleTableObject, SubsampleImagesTableObject
from webservices.chemicalanalysis import ChemicalAnalysisObject, ChemicalAnalysisTableObject
from webservices.db import MetPet


#direct stdout to stderr so that it is logged by the webserver
sys.stdout = sys.stderr


def chemical_analysis(request, chemical_analysis_id):
    email = request.GET.get('email', None)
    api_key = request.GET.get('api_key', None)
    api = MetPet(email, api_key).api

    chem_analysis =ChemicalAnalysisObject(chemical_analysis_id)
    chem_analysis_obj = api.chemical_analysis.get(chemical_analysis_id).data

    subsample = api.subsample.get_by_uri(chem_analysis_obj['subsample']).data

    if chem_analysis:
        del chem_analysis.attributes['analysis_date']
        data = {
            'chemical_analysis': chem_analysis.attributes,
            'subsample_id': subsample['subsample_id'],
            'sample_id': subsample['sample'].split('/')[-2]
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Chemical Analysis does not exist")


def sample_images(request, sample_id):
    sampleimagesobj = SampleImagesObject(sample_id)

    if sampleimagesobj.exists():
        return HttpResponse(sampleimagesobj.json())
    else:
        return HttpResponse("Sample does not Exist")



'''S2S webservice view'''
#Main faceted serach view
def metpetdb(request):

    formattype=request.GET.get('format','json')

    returntype=request.GET.get('returntype','sampleresults')

    rocktype_id=request.GET.get('rocktype_id','')

    country=request.GET.get('country','')

    owner_id=request.GET.get('owner_id','')

    mineral_id=request.GET.get('mineral_id','')

    region_id=request.GET.get('region_id','')

    metamorphic_grade_id=request.GET.get('metamorphic_grade_id','')

    metamorphic_region_id=request.GET.get('metamorphic_region_id','')

    publication_id= request.GET.get('publication_id','')

    if rocktype_id!='':
        rocktype_id_list=rocktype_id.split(',')
    else:
        rocktype_id_list=[]

    if mineral_id!='':
        mineral_id_list=mineral_id.split(',')
    else:
        mineral_id_list=[]

    if owner_id!='':
        owner_id_list=owner_id.split(',')
    else:
        owner_id_list=[]

    if country!='':
        country_list=country.split(',')
    else:
        country_list=[]

    if region_id!='':
        region_id_list=region_id.split(',')
    else:
        region_id_list=[]

    if metamorphic_region_id!='':
        metamorphic_region_id_list=metamorphic_region_id.split(',')
    else:
        metamorphic_region_id_list=[]

    if metamorphic_grade_id!='':
        metamorphic_grade_id_list=metamorphic_grade_id.split(',')
    else:
        metamorphic_grade_id_list=[]

    if publication_id!='':
        publication_id_list=publication_id.split(',')
    else:
        publication_id_list=[]


    samples=SampleQuery(rock_type=rocktype_id_list,country=country_list,owner_id=owner_id_list,mineral_id=mineral_id_list,region_id=region_id_list,metamorphic_grade_id=metamorphic_grade_id_list, metamorphic_region_id=metamorphic_region_id_list, publication_id=publication_id_list)
    #sample_test = SampleQuery(rock_type=[3,], country=[], owner_id=[139,], mineral_id=[3,], region_id=[52,], metamorphic_grade_id=[17,], metamorphic_region_id=[], publication_id=[])
    if returntype=='rocktype_facet':
        return HttpResponse(getFacetJSON(samples.rock_type_facet()), content_type="application/json")
    elif returntype=='country_facet':
        return HttpResponse(getFacetJSON(samples.country_facet()), content_type="application/json")
    elif returntype=='mineral_facet':
        return HttpResponse(getFacetJSON(samples.mineral_facet()), content_type="application/json")
    elif returntype=='region_facet':
        return HttpResponse(getFacetJSON(samples.region_facet()), content_type="application/json")
    elif returntype=='owner_facet':
        return HttpResponse(getFacetJSON(samples.owner_facet()), content_type="application/json")
    elif returntype=='metamorphicgrade_facet':
        return HttpResponse(getFacetJSON(samples.metamorphic_grade_facet()), content_type="application/json")
    elif returntype=='metamorphicregion_facet':
        return HttpResponse(getFacetJSON(samples.metamorphic_region_facet()), content_type="application/json")
    elif returntype== 'publication_facet':
        return HttpResponse(getFacetJSON(samples.publication_facet()), content_type="application/json")
    elif returntype=='map':
        #q=test.get_main_brief()
        return HttpResponse(getAllJSON(samples.get_main_brief()), content_type="application/json")
    else:
        cursor=con.cursor()
        cursor.execute(samples.get_count())
        sample_count=cursor.fetchall()
        #this is currently a hack to pass a html element containing the sample_count
        htmlCount="<div id='sampleCount' display:'none'>"+str(sample_count[0][0])+"</div>"
        print htmlCount
        if sample_count>500:
            return HttpResponse(getSampleResults(samples.get_main(500))+htmlCount)
        else:
            return HttpResponse(getSampleResults(samples.get_main(500)))

#Not sure if below is used for anything right now
#Function to format oxides by subscripting digits
def formatOxide(species):
        retStr=""
        i=0
        while(i<len(species)):
                if species[i].isdigit():
                        retStr+='<sub>'+species[i]+'</sub>'
                else:
                        retStr+=species[i]
                i+=1
        return retStr
