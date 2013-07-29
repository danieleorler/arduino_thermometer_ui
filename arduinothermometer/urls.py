from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'temperature.views.index'),
                       url(r'^temperature/$', 'temperature.views.index'),
                       url(r'^temperature/(?P<sensor>\w+)/$', 'temperature.views.index'),
                       url(r'^stats/(?P<sensor>\w+)/(?P<type>\w+)/$', 'temperature.views.stats'),
                       url(r'^stats/(?P<sensor>\w+)/(?P<type>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/$', 'temperature.views.manualStats'),
                       url(r'^indicators/(?P<sensor>\w+)/(?P<type>\w+)/$', 'temperature.views.indicators'),
    # Examples:
    # url(r'^$', 'arduinothermometer.views.home', name='home'),
    # url(r'^arduinothermometer/', include('arduinothermometer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
