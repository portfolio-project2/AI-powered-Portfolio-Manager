from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),  # Example route
    path('help/', views.help_center, name='help_center'),  # Example route
    path('dashboard/', views.dashboard, name='dashboard'),  # Example route
]