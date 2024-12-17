from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deletedAt__isnull=True)

class AllUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Role(models.Model):
    idRole = models.AutoField(primary_key=True)
    poste = models.CharField(max_length=255)

    def __str__(self):
        return self.poste

class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    idRole = models.ForeignKey(Role, on_delete=models.CASCADE)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    genre = models.CharField(max_length=10, blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    passwordVersion = models.IntegerField(default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = AllUserManager()

    def __str__(self):
        return f"{self.firstname} {self.name}"

class UserPreference(models.Model):
    idPreference = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Preferences for {self.idUser.login}"