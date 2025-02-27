from django.contrib.auth.models import User
# Django’s built-in user model
from django.db import models
# create and manage database models.

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        # first value is stored in the database,
        # and the second value is the human-readable name.
        ('patient', 'Patient'),
        ('admin', 'Administrative Staff'),
        ('provider', 'Healthcare Provider'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Each user has exactly one UserProfile, and the profile has exactly one user.
    # If a user is deleted, their profile will also be deleted
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)



# Create a signal to create/update the user profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User) # connects post_save signal to the create_user_profile function for User model.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


