# this line is to import path function from django.urls package
from django.urls import path
# this is to import views.py and . means from the same subfolder complains
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]