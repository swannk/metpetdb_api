from django.http import HttpResponse, HttpResponseRedirect
from webservices.utility import *
from webservices.sample import SampleObject
from webservices.subsample import SubsampleObject, SubsampleTableObject, SubsampleImagesTableObject
from webservices.chemicalanalysis import ChemicalAnalysisObject, ChemicalAnalysisTableObject


def sample(request, sample_id):
	sampleobj = SampleObject(sample_id)
	if sampleobj.exists():
		return HttpResponse(sampleobj.json())
	else:
		return HttpResponse("sample does not exist")


def subsample(request, subsample_id):
	subsampleobj =SubsampleObject(subsample_id)
	if subsampleobj.exists():
		return HttpResponse(subsampleobj.json())
	else: 
		return HttpResponse("subsample does not exist")


def chemicalanalysis(request, chemical_analysis_id):
	chemanalysisobj =ChemicalAnalysisObject(chemical_analysis_id)
	if chemanalysisobj.exists():
		return HttpResponse(chemanalysisobj.json())

def subsample_images(request, subsample_id):
    subsampleImagesTableObj = SubsampleImagesTableObject(subsample_id)
    return HttpResponse(subsampleImagesTableObj.json())


def subsamples(request, sample_id):
	subsampleTableObj = SubsampleTableObject(sample_id)
	return HttpResponse(subsampleTableObj.json())

    
def chemical_analyses(request, subsample_id):
    chemicalAnalysisTableObj = ChemicalAnalysisTableObject(subsample_id)
    return HttpResponse(chemicalAnalysisTableObj.json())


# uses size and id
# sizes - 1,2,3,4 --> from mobile to original
'''def images(request):

	size=request.GET.get('size','')
	attribute_id =request.GET.get('id','')

	cursor=db.cursor()
	#mobile image - checksum_mobile
	if size==1:

		image_data=cursor.execute("SELECT  ")

	#Thumbnail images
	elif size==2:

		image_data=cursor.execute("SELECT")

	#pop up images
	elif size==3:

		image_data=cursor.execute("SELECT")

	#original images
	elif size==4:

		image_data=cursor.execute("SELECT")

	else: 

		HTTPResponse("please follow the correct URL parameters")'''



