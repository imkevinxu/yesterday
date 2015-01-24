from django.conf.urls import url

from .views import home, story

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^story/(?P<uuid>.+)/$', story, name='story'),
]
