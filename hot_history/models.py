from django.db import models
from hot_users.models import User
from hot_rooms.models import CommandeRoom
from hot_services.models import CommandeService

class typeHistorique(models.Model):
    idType = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    # 1: Commande Room, 2: Commande Service

    def __str__(self):
        return self.name

class Historique(models.Model):
    idHistorique = models.AutoField(primary_key=True)
    idAdmin = models.ForeignKey(User, on_delete=models.CASCADE)
    idType = models.ForeignKey(typeHistorique, on_delete=models.CASCADE)
    idCommandeRoom = models.ForeignKey(CommandeRoom, on_delete=models.SET_NULL, null=True, blank=True)
    idCommandeService = models.ForeignKey(CommandeService, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Historique {self.idHistorique}"