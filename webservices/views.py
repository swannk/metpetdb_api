from django.http import HttpResponse
from webservices.models import Users
def index(request):
	str1=""
	for p in Users.objects.raw('SELECT * FROM Users'):
		str1=str1+unicode(p.country)+"\n"
    	return HttpResponse(str1)
