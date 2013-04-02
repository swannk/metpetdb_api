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