from django.db import models
from hot_users.models import User
from hot_clients.models import Client
from hot_services.models import Status
from hot_rooms.validators.price import validate_positive

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deletedAt__isnull=True)

class AllRoomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Room(models.Model):
    idRoom = models.AutoField(primary_key=True)
    idAdmin = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subTitle = models.CharField(max_length=255, blank=True, null=True)
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
    def __str__(self):
        return self.title

class CommandeRoom(models.Model):
    idCommande = models.AutoField(primary_key=True)
    idRoom = models.ForeignKey(Room, on_delete=models.CASCADE)
    idClient = models.ForeignKey(Client, on_delete=models.CASCADE)
    idAdmin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    idStatus = models.ForeignKey(Status, on_delete=models.CASCADE)
    DateStart = models.DateTimeField()
    DateEnd = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Commande {self.idCommande} for Room {self.idRoom.title}"
