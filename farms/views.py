import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Farm, BlockchainLog

# --- AUTHENTICATION ---
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

# --- DASHBOARD ---
@login_required
def dashboard(request):
    if request.method == 'POST':
        Farm.objects.create(
            user=request.user,
            name=request.POST.get('farm_name', 'My Farm'), 
            intended_crop=request.POST.get('intended_crop'),
            nitrogen=request.POST.get('n', 0),
            phosphorus=request.POST.get('p', 0),
            potassium=request.POST.get('k', 0),
            ph_level=request.POST.get('ph', 7.0)
        )
        messages.success(request, "Farm added successfully!")
        return redirect('dashboard')
    
    farms = Farm.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'farms': farms})

# --- PREDICTION LOGIC ---
@login_required
def predict_crop(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    
    # Random logic for hackathon demonstration
    score = random.randint(75, 98)
    status = "Optimal" if score > 80 else "Attention Needed"
    
    # Log to Blockchain Model
    BlockchainLog.objects.create(
        action=f"Market Sync Analysis: {farm.name}", 
        hash="0x" + str(random.getrandbits(64))
    )
    
    return render(request, 'predict_result.html', {
        'farm': farm, 
        'sync_score': score, 
        'status': status
    })

# --- OTHER FEATURES ---
def disease_lab(request):
    diagnosis = None
    if request.method == 'POST' and request.FILES.get('image'):
        results = ["Healthy Leaf", "Leaf Rust detected", "Early Blight identified"]
        diagnosis = random.choice(results)
        BlockchainLog.objects.create(action="AI Disease Scan", hash="0x" + str(random.getrandbits(64)))
    return render(request, 'disease_lab.html', {'diagnosis': diagnosis})

def blockchain_ledger(request):
    logs = BlockchainLog.objects.all().order_by('-timestamp')
    return render(request, 'blockchain_ledger.html', {'logs': logs})