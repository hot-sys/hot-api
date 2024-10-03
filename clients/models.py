from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta

class UserClient(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    genre = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address_client = models.TextField(blank=True, null=True)
    position_lat = models.FloatField(blank=True, null=True)
    position_long = models.FloatField(blank=True, null=True)
    password_client = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    validation_client = models.BooleanField(default=False)
    code = models.BigIntegerField(blank=True, null=True)
    status_client = models.BooleanField(default=False)
    photo = models.CharField(max_length=255, blank=True, null=True)

    def set_password(self, raw_password):
        self.password_client = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_client)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ActivateAccount(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        existing_entry = ActivateAccount.objects.filter(email=self.email).first()
        
        if existing_entry:
            existing_entry.delete()

        self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email