
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>[a-zA-Z0-9]+)/(?P<weibo_id>[a-zA-Z0-9]+)/$', views.demo, name='demo')
]
