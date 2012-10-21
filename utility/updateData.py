import urllib2


def getSamples():
        fileObj=open('../web/samples/samples.json','w')
        response = urllib2.urlopen('http://metpetdb.rpi.edu/metpetdb-py/webservices/samples')
        fileObj.write(str(response.read()))

def getChemicalAnalyses():
        fileObj=open('../web/chemical_analyses/chemical_analyses.json','w')
        response = urllib2.urlopen('http://metpetdb.rpi.edu/metpetdb-py/webservices/chemicalanalyses')
        fileObj.write(str(response.read()))




if __name__=="__main__":
        getSamples()
        getChemicalAnalyses()

