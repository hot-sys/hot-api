from django.db import models

class UserAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    poste = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.name}"
