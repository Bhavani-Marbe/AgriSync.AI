import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dotenv import load_dotenv
from PIL import Image

# Import your custom models and utilities
from .models import Farm
from .utils import get_coords_from_image, get_environmental_data, calculate_market_logic

# Load environment variables (API Keys)
load_dotenv()

# --- HELPER FUNCTIONS ---

def get_live_weather(lat, lon):
    """Fetches real-time weather from OpenWeatherMap using the .env API Key."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'condition': data['weather'][0]['main'],
                'city': data.get('name', 'Local Area')
            }
    except Exception as e:
        print(f"Weather API Error: {e}")
    
    # Fallback if API fails
    return {'temp': 28, 'humidity': 65, 'condition': 'Clear', 'city': 'Unknown'}


# --- VIEW FUNCTIONS ---

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        image = request.FILES.get('farm_image')
        # Simulate Satellite GPS extraction from image
        lat, lon = get_coords_from_image(image) if image else (request.POST.get('lat'), request.POST.get('lon'))
        
        Farm.objects.create(
            user=request.user,
            farm_name=request.POST.get('farm_name'),
            image=image,
            intended_crop=request.POST.get('intended_crop'),
            latitude=lat,
            longitude=lon,
            soil_type=request.POST.get('soil_type'),
            nitrogen=request.POST.get('n', 0),
            phosphorus=request.POST.get('p', 0),
            potassium=request.POST.get('k', 0),
            ph_level=request.POST.get('ph', 7.0)
        )
        messages.success(request, "Farm added to AgriSync successfully!")
        return redirect('dashboard')
    
    farms = Farm.objects.filter(user=request.user)
    return render(request, 'farms/dashboard.html', {'farms': farms})

@login_required
def predict_crop(request, farm_id):
    """Combines Soil data, Market logic, and Live Weather for the final report."""
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    
    # Get live weather for the report
    weather = get_live_weather(farm.latitude, farm.longitude)
    
    # Use your market logic from utils.py
    crop, advice, saturation, is_risky = calculate_market_logic(farm)
    
    # Additional Storage Advice based on humidity
    humidity = weather.get('humidity', 50)
    if humidity > 70:
        storage_advice = "High Humidity Detected. Use airtight silos and fungal retardants."
    elif humidity < 30:
        storage_advice = "Dry Conditions. Ensure proper ventilation to prevent seed cracking."
    else:
        storage_advice = "Standard Storage. Keep in a cool, shaded area."

    return render(request, 'farms/result.html', {
        'farm': farm,
        'crop': crop,
        'advice': advice,
        'saturation': saturation,
        'is_risky': is_risky,
        'env': weather,
        'storage_advice': storage_advice
    })

def disease_lab(request):
    """Simulated AI for plant disease detection (Python 3.14 compatible)."""
    result = ''
    if request.method == 'POST' and request.FILES.get('leaf_image'):
        image = request.FILES['leaf_image']
        name = image.name.lower()
        
        # Simulated Detection Logic
        if 'spot' in name or 'brown' in name:
            result = "Brown Spot (Fungal)"
        elif 'yellow' in name or 'wilt' in name:
            result = "Bacterial Wilt"
        else:
            result = "Healthy Leaf (No Disease Detected)"

    return render(request, 'farms/disease_lab.html', {'result': result})

def market_trends(request):
    return render(request, 'farms/market_trends.html')

def blockchain_ledger(request):
    return render(request, 'farms/blockchain_ledger.html')