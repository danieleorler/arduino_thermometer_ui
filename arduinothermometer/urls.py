from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^temperature/$', 'temperature.views.index'),
                       url(r'^temperature/(?P<sensor>\w+)/$', 'temperature.views.index'),
                       url(r'^stats/(?P<sensor>\w+)/$', 'temperature.views.stats')
    # Examples:
    # url(r'^$', 'arduinothermometer.views.home', name='home'),
    # url(r'^arduinothermometer/', include('arduinothermometer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)