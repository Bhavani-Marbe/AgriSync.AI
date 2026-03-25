from django.contrib import admin
from django.urls import path, include
from farms import views # Keep this for register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    
    # This ONE line handles all the farm pages (Dashboard, Lab, Trends)
    path('', include('farms.urls')), 
]