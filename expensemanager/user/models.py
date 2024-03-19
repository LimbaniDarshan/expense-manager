from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=12)
    
    def update_profile(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()
    class Meta:
        db_table = 'user'