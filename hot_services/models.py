from django.db import models
from hot_users.models import User
from hot_clients.models import Client

class Status(models.Model):
    idStatus = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    idService = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class ServiceItem(models.Model):
    idItem = models.AutoField(primary_key=True)
    idService = models.ForeignKey(Service, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subTitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    unity = models.CharField(max_length=50, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class CommandeService(models.Model):
    idCommande = models.AutoField(primary_key=True)
    idItem = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)
    idClient = models.ForeignKey(Client, on_delete=models.CASCADE)
    idStatus = models.ForeignKey(Status, on_delete=models.CASCADE)
    idAdmin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Commande {self.idCommande} for Service {self.idItem.title}"
