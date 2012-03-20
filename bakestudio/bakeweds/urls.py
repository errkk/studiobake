from django.conf.urls.defaults import *
from django.conf import settings
from django.views import static
from bakeweds.views import index

urlpatterns = patterns('',

	url(r'^$', index, name='index'),

	url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
)