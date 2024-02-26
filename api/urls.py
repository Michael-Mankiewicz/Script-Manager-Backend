from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('address_change',views.address_change)
]