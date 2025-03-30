from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    path('market_news/', views.market_news, name='market_news'),
    path('financial_goals/', views.financial_goals, name='financial_goals'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('help_center/', views.help_center, name='help_center'), 
    
]