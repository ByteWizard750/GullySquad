from django.db import models
from django.conf import settings

class Squad(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_squads')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SquadMember', related_name='squads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    max_members = models.PositiveIntegerField(default=11)  # Default cricket team size
    
    def __str__(self):
        return self.name

class SquadMember(models.Model):
    ROLE_CHOICES = (
        ('captain', 'Captain'),
        ('vice_captain', 'Vice Captain'),
        ('member', 'Member'),
    )
    
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('squad', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.squad.name}" 