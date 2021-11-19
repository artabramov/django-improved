from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
import random, string

# Create your models here.
class User(AbstractUser):

    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    auth_key = models.CharField(max_length=128, unique=False, blank=True)
    auth_expires = models.DateTimeField(default=(now() + timedelta(hours=24)))

    def set_expires(self):
        self.is_active = False
        self.auth_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(80))
        self.auth_expires = now() + timedelta(hours=24)
        self.save()

    def is_expired(self):
        if self.auth_expires < now():
            return True
        return False

    def ban(self):
        self.is_active = False
        self.save()
        

class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский')
    )

    user = models.OneToOneField(
        User, 
        unique=True, 
        null=False, 
        db_index=True, 
        on_delete=models.CASCADE
    )

    tags = models.CharField(verbose_name='теги', max_length=128, blank=True)

    bio = models.TextField(verbose_name='о себе', max_length=512, blank=True)

    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


