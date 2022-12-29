# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import *
#from django.views.generic import RedirectView

from helpers import here

urlpatterns = patterns('ywot.views',
    ### Web page:
    # Main
    url(r'^$', 'home', name='home'),
    url(r'^risd/$', 'func_risd_2023', name='func_risd_2023'),

    
    ### Worlds:
    # World management
    url(r'^ajax/protect/$', 'protect', name='protect'),
    url(r'^ajax/unprotect/$', 'unprotect', name='unprotect'),
    url(r'^ajax/coordlink/$', 'coordlink', name='coordlink'),
    url(r'^ajax/urllink/$', 'urllink', name='urllink'),
)

#urlpatterns += patterns('',
#    (r'^favicon\.ico$', RedirectView, {'url': '/static/favicon.png'}),
#)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': here('static')}),
    )
 
