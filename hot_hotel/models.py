from django.db import models

class HotelInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    color = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    adress = models.TextField(blank=True, null=True)
    homeImage = models.JSONField()  # Stores an array of image URLs or paths

    def __str__(self):
        return self.name
