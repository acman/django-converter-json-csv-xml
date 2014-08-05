from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'core.views',
    url(r'^$', 'home', name='home'),

    # url(r'^admin/', include(admin.site.urls)),
)
