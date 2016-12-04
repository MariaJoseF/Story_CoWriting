from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.FooterView, name='footer'),
    url(r'^$', views.HeaderView, name='header'),

]


