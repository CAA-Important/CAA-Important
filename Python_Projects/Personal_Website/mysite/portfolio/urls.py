from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'portfolio'
urlpatterns = [
    path('', views.PortfolioView.as_view(), name="portfolio_app"),
]