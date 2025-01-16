from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deletedAt__isnull=True)

class AllClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Client(models.Model):
    idClient = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(null=True)
    genre = models.CharField(max_length=10, blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    cin = models.CharField(max_length=50, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = AllClientManager()
    def __str__(self):
        return f"{self.firstName} {self.name}"
