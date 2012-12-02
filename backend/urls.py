from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
   url(r'^$'                , 'backend.views.home'      ),
   url(r'^/$'               , 'backend.views.home'      ),
   url(r'^home/$'           , 'backend.views.home'      ),
   url(r'^editSong/$'       , 'backend.views.editSong'  ),
   url(r'^viewSong$'        , 'backend.views.viewSong'  ),
   url(r'^deleteSong$'      , 'backend.views.deleteSong'),

   url(r'^toggleSongToCollection/$', 'backend.views.toggleSongToCollection'),
   url(r'^toggleVote/$'     , 'backend.views.toggleVote'),

   url(r'^printSongs/$'     , 'backend.views.printSongs'),
   url(r'^search/$'         , 'backend.views.search'),

   url(r'^user_login/$'     , 'backend.views.userLogin'),
   url(r'^createUser/$'     , 'backend.views.createUser'),
   
   url(r'^selectable/'      , include('selectable.urls')), 
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',{'post_change_redirect': '/start/'}),
    url(r'^password_change_done/$', 'django.contrib.auth.views.password_change_done'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # file stuff
    (r'^static/(?P<path>.*html)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,'show_indexes' : True}),
    (r'^static/(?P<path>.*css)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,'show_indexes' : True}),
    (r'^static/(?P<path>.*jpg)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,'show_indexes' : True}),
    (r'^static/(?P<path>.*png)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,'show_indexes' : True}),
    (r'^static/(?P<path>.*js)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,'show_indexes' : True}),
    (r'^static/(?P<path>.*pdf)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,'show_indexes' : True}),
    (r'^static/(?P<path>.*ttf)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,'show_indexes' : True}),
)
