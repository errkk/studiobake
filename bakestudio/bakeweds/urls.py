# -- coding: utf-8 --
from django.conf.urls.defaults import *
from django.conf import settings
from django.views import static
from bakeweds.views import index, detail, Login, Logout, DeleteComment, volunteer

urlpatterns = patterns('',

	url(r'^$', index, name='index'),
	url(r'^bake/(?P<id>\d+)$', detail, name='detail'),
	url(r'^delete_comment/(?P<id>\d+)$', DeleteComment, name='delete_comment'),
	url(r'^volunteer/$', volunteer, name='volunteer'),

	url(r'^login/$', Login, name='Login'),
	url(r'^logout/$', Logout, name='Logout'),
	

	url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
	url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
)