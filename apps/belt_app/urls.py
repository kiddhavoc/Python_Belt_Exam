from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^dashboard', views.dash),
    url(r'^destinations/(?P<number>\d+)', views.destination),
    url(r'^add', views.add),
    url(r'^process', views.process),
    url(r'^join/(?P<number>\d+)', views.join),
]