from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
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
        