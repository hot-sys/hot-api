from django.db import models
from hot_users.models import User
from hot_clients.models import Client
from hot_services.models import Status
from hot_rooms.validators.price import validate_positive
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset().filter(deletedAt__isnull=True)
        return queryset
class AllRoomManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class AllCommandManager(models.Manager):
    def get_queryset(self):
        today = timezone.now().date()
        queryset = super().get_queryset().filter(DateStart__date__gte=today)
        # queryset = super().get_queryset()
        return queryset

class Room(models.Model):
    idRoom = models.AutoField(primary_key=True, db_index=True)
    idAdmin = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    subTitle = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(validators=[validate_positive])
    available = models.BooleanField(default=True)
    dateAvailable = models.DateTimeField(blank=True, null=True)
    info = models.JSONField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = AllRoomManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class RoomImage(models.Model):
    idImage = models.AutoField(primary_key=True)
    idRoom = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.idImage} for Room {self.idRoom.title}"

class CommandeRoom(models.Model):
    idCommande = models.AutoField(primary_key=True)
    idRoom = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, db_index=True)
    idClient = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, db_index=True)
    idAdmin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True, blank=True)
    idStatus = models.ForeignKey(Status, on_delete=models.CASCADE, db_index=True, null=True)
    DateStart = models.DateTimeField(db_index=True)
    DateEnd = models.DateTimeField()
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    payed = models.IntegerField(default=0, null=True)
    received = models.BooleanField(null=True, default=False)
    dateReceived = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    objects = AllCommandManager()

    def __str__(self):
        return f"Commande {self.idCommande} for Room {self.idRoom.title}"
