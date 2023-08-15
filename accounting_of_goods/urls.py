from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
	path('', views.index, name='main'),
	path('contact/', views.contact, name='contact'),
	path('admin/', views.adm, name='admin'),
	path('receipt/', views.receipt, name='receipt'),
	path('consumption/', views.consumption, name='consumption')
]