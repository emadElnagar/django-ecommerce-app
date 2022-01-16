from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    shop = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ CREATE PROFILE AUTOMATICALLY AFTER USER SIGNUP """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_delete, sender= Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ DELETE PROFILE IMAGE AUTOMATICALLY AFTER DELETING PROFILE """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
