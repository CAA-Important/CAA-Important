from django.urls import path

from . import views

app_name = 'hello'
urlpatterns = [
    path('', views.HelloAppView.as_view(), name='hello_app'),
    path('hello/info', views.HelloInfoView.as_view(), name='hello_info'),
]