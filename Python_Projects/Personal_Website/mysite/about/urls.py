from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'about'
urlpatterns = [
    path('', views.AboutView.as_view(), name="about_app"),
]