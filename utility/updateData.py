import urllib2
import sys


def getSamples(filePath):
        response = urllib2.urlopen('http://metpetdb.rpi.edu/metpetdb-py/webservices/samples')
	fileObj=open(filePath+'web/samples/samples.json','w')
	fileObj.write(str(response.read()))

def getChemicalAnalyses(filePath):
        response = urllib2.urlopen('http://metpetdb.rpi.edu/metpetdb-py/webservices/chemicalanalyses')
        fileObj=open(filePath+'web/chemical_analyses/chemical_analyses.json','w')
	fileObj.write(str(response.read()))




if __name__=="__main__":
	try:
		filePath=sys.argv[1]
		getSamples(filePath)
        	getChemicalAnalyses(filePath)
	except Exception as e:
		print "Exception :"+str(e)+" Please enter filePath. Eg: /home/user/projectfolder/"

