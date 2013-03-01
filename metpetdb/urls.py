from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
url(r'^webservices/$', 'webservices.views.index'),
url(r'^webservices/samples$', 'webservices.views.samples'),
url(r'^webservices/chemicalanalyses$', 'webservices.views.chemical_analyses'), 
url(r'^api/sample/(\d+)/$','webservices.api.sample'), 
url(r'^api/subsample/(\d+)/$','webservices.api.subsample'), 
url(r'^api/subsample/(\d+)/images/$','webservices.api.subsample_images'), 
url(r'^api/subsamples/(\d+)/$','webservices.api.subsamples'), 
url(r'^api/chemicalanalysis/(\d+)/$', 'webservices.api.chemical_analysis'), 
url(r'^api/chemicalanalyses/(\d+)/$', 'webservices.api.chemical_analyses'), 
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
