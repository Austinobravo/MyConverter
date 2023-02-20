from django.urls import path
from . import views

#Converter Urls
urlpatterns = [
    path('', views.home, name='home'),
    path('/details/', views.details, name='details'),

]