from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('predict/<int:farm_id>/', views.predict_crop, name='predict_crop'),
    path('disease-lab/', views.disease_lab, name='disease_lab'),
    path('market-trends/', views.market_trends, name='market_trends'),
    path('blockchain/', views.blockchain_ledger, name='blockchain_ledger'),
]