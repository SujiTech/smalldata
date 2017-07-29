from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView


urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^weibo-demo/', include('demo.urls')),
    url(r'^admin/', admin.site.urls),
]
