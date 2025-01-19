from django.db import models
from hot_users.models import User
from hot_clients.models import Client

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deletedAt__isnull=True)

class AllManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class AllCommandManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset().filter(received=False)
        return queryset

class Status(models.Model):
    idStatus = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    # 1: Reserved, 2: Canceled, 3: Confirmed, 4: Pending
    def __str__(self):
        return self.name

class Service(models.Model):
    idService = models.AutoField(primary_key=True, db_index=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = AllManager()
    def __str__(self):
        return self.name

class ServiceItem(models.Model):
    idItem = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    idService = models.ForeignKey(Service, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subTitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    unity = models.CharField(max_length=50, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = AllManager()
    def __str__(self):
        return self.title

class ItemImage(models.Model):
    idImage = models.AutoField(primary_key=True)
    idItem = models.ForeignKey(ServiceItem, related_name='images', on_delete=models.CASCADE)
    image = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.idImage} for item {self.idItem.title}"

class CommandeService(models.Model):
    idCommande = models.AutoField(primary_key=True)
    idCommandeCommune = models.CharField(max_length=255, blank=True, null=True)
    idItem = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)
    idClient = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    idStatus = models.ForeignKey(Status, on_delete=models.CASCADE)
    idAdmin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField()
    total = models.IntegerField(default=0)
    received = models.BooleanField(null=True, default=False)
    dateReceived = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    objects = AllCommandManager()
    def __str__(self):
        return f"Commande {self.idCommande} for Service {self.idItem.title}"
