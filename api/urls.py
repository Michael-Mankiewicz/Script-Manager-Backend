from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test),
    path('report', views.report),
    path('string', views.string),
    path('settings', views.settings),
    path('scripts', views.script_list)
]