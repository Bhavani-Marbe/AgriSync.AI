import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Farm

def register(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')
    
    return render(request, 'registration/register.html')

def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    farms = Farm.objects.filter(user=request.user)
    # Corrected path for namespaced templates
    return render(request, 'farms/dashboard.html', {'farms': farms})

@login_required
def predict_crop(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    
    # Analysis Logic
    score = random.randint(80, 99)
    status = "Optimal" if score > 85 else "Stable"
    
    context = {
        'farm': farm,
        'sync_score': score,
        'status': status,
        'recommendation': f"Soil metrics for {farm.intended_crop} are looking excellent.",
    }
    return render(request, 'farms/predict_crop.html', context)

@login_required
def market_trends(request):
    """
    Logic for Market Trends feature
    """
    # Simulated market data
    trends = [
        {'crop': 'Wheat', 'price': '₹2,100', 'change': '+2.5%'},
        {'crop': 'Rice', 'price': '₹3,500', 'change': '-1.2%'},
        {'crop': 'Cotton', 'price': '₹6,200', 'change': '+5.0%'},
    ]
    return render(request, 'farms/market_trends.html', {'trends': trends})

@login_required
def disease_lab(request):
    diagnosis = "No active threats detected in your region."
    return render(request, 'farms/disease_lab.html', {'diagnosis': diagnosis})

@login_required
def blockchain_ledger(request):
    logs = [{'date': '2026-03-26', 'action': 'System Sync', 'hash': '0x94f...'}]
    return render(request, 'farms/blockchain_ledger.html', {'logs': logs})