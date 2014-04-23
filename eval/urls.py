from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eval.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^main', 'hlidskjalf.views.index'),
    url(r'^run/(?P<id>\d+)', 'hlidskjalf.views.details'),
    url(r'^save/(?P<id>\d+)/(?P<value>\d+)', 'hlidskjalf.views.save'),
)
