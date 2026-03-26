@login_required
def dashboard(request):
    # Logic...
    farms = Farm.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'farms': farms})

@login_required
def predict_crop(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    # Logic...
    return render(request, 'predict_result.html', {
        'farm': farm, 
        'sync_score': random.randint(75, 98), 
        'status': "Optimal"
    })