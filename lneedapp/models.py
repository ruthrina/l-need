from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class loginLogic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_login = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username  # Display the username as the profile's representation

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        loginLogic.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserProfile(models.Model):
    
    username = models.CharField(max_length=150, default=True)
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(default=0)
    profileImage= models.ImageField(upload_to="profile_images/", blank=True)    
