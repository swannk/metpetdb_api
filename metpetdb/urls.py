from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
url(r'^webservices/$', 'webservices.views.index'),
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
