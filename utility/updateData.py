import urllib2
import sys


def getSamples(filePath):
        fileObj=open(filePath+'web/samples/samples.json','w')
        response = urllib2.urlopen('http://metpetdb.rpi.edu/metpetdb-py/webservices/samples')
        fileObj.write(str(response.read()))

def getChemicalAnalyses(filePath):
        fileObj=open(filePath+'web/chemical_analyses/chemical_analyses.json','w')
        response = urllib2.urlopen('http://metpetdb.rpi.edu/metpetdb-py/webservices/chemicalanalyses')
        fileObj.write(str(response.read()))




if __name__=="__main__":
	if sys.argv[1]!='':
		filePath=sys.argv[1]
	else:
		print "Please enter filePath. Eg: /home/user/projectfolder/"
		sys.exit()
        getSamples(filePath)
        getChemicalAnalyses(filePath)

