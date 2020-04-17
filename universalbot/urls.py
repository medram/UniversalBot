from django.urls import path, include

from universalbot import views

urlpatterns = [
    path('', views.home, name='home')
]

