# this line is to import path function from django.urls package
from django.urls import path
# this is to import views.py and . means from the same subfolder complains
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_complaint/', views.create_complaint, name='create_complaint'),
    path('complaint_list/', views.complaint_list, name='complaint_list'),
    
    # yaha kuch naya hai <int:pk> yeh path parameter hai int type ka 
    path('complaint/<int:pk>/', views.complaint_details, name='complaint_details'),
]