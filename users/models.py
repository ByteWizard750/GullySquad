from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('all_rounder', 'All Rounder'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    matches_played = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.username 