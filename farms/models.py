from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="My Farm") 
    location = models.CharField(max_length=100, default="Unknown")
    intended_crop = models.CharField(max_length=100, blank=True, null=True)
    nitrogen = models.FloatField(default=0.0)
    phosphorus = models.FloatField(default=0.0)
    potassium = models.FloatField(default=0.0)
    ph_level = models.FloatField(default=7.0)
    soil_type = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='farm_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class BlockchainLog(models.Model):
    action = models.CharField(max_length=255)
    hash = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.timestamp}"