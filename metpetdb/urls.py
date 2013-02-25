from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
url(r'^webservices/$', 'webservices.views.index'),
url(r'^webservices/samples$', 'webservices.views.samples'),
url(r'^webservices/chemicalanalyses$', 'webservices.views.chemical_analyses'), 
url(r'^api/sample/(\d+)/$','webservices.views.sample'), 
url(r'^api/subsample/(\d+)/$','webservices.views.subsample'), 
url(r'^api/subsamples/(\d+)/$','webservices.views.subsamples'), 
url(r'^api/chemicalanalysis/(\d+)/$', 'webservices.views.chemicalanalysis'), 
url(r'^api/chemicalanalyses/(\d+)/$', 'webservices.views.chemicalanalyses'), 
url(r'^api/metpetdb/$','webservices.views.metpetdb'), 
    # Examples:
    # url(r'^$', 'metpetdb.views.home', name='home'),
    # url(r'^metpetdb/', include('metpetdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns+=staticfiles_urlpatterns()
