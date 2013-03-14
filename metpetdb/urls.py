from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('', 
url(r'^webservices/sample/(\d+)/json/$','webservices.views.sample'),
url(r'^webservices/sample/(\d+)/$','webservices.views.sample'),
url(r'^webservices/subsample/(\d+)/json/$','webservices.views.subsample'), 
url(r'^webservices/subsample/(\d+)/$','webservices.views.subsample'), 
url(r'^webservices/chemicalanalysis/(\d+)/json$', 'webservices.views.chemicalanalysis'), 
url(r'^webservices/chemicalanalysis/(\d+)/$', 'webservices.views.chemicalanalysis'), 
url(r'^api/metpetdb/$','webservices.views.metpetdb'), 
#sample list url
url(r'^webservices/samplelist/$', 'webservices.views.samplelist', name='samplelist'),
url(r'^$', 'webservices.views.index', name='index'),
url(r'^search/$', 'webservices.views.search', name='search'),
#below URLs- Not sure if these are used anywhere as of now
url(r'^webservices/samples$', 'webservices.views.samples'),
url(r'^webservices/chemicalanalyses$', 'webservices.views.chemical_analyses'),


    # Examples:
    # url(r'^$', 'metpetdb.views.home', name='home'),
    # url(r'^metpetdb/', include('metpetdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns+=staticfiles_urlpatterns()
