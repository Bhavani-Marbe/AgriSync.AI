from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    
    # Dashboard & Logic
    path('', views.dashboard, name='dashboard'),
    path('predict/<int:farm_id>/', views.predict_crop, name='predict_crop'),
    
    # Tools
    path('market-trends/', views.market_trends, name='market_trends'),
    path('disease-lab/', views.disease_lab, name='disease_lab'),
    path('ledger/', views.blockchain_ledger, name='blockchain_ledger'),
]