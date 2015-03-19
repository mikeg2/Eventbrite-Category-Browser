from django.conf.urls import patterns, include, url
from django.contrib import admin
from event_browser.views import category

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eventbrite_app_1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',  category), # refactor
)
