from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    BOOKING_SITE_ROLES = (
        ("ad", "Admin"),
        ("cu", "Customer"),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=2, choices=BOOKING_SITE_ROLES, default='cu')


    def __str__(self):
        return self.get_role() + ' ' + self.user.username


    def get_role(self):
        roles_dict = dict(self.BOOKING_SITE_ROLES)
        return roles_dict[self.role]
    

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
             instance.profile.save()