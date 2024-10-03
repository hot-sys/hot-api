from django.db import models

class TypeActivite(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Activite(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('clients.UserClient', on_delete=models.CASCADE)
    type_activite = models.ForeignKey(TypeActivite, on_delete=models.CASCADE)
    admin = models.ForeignKey('adminuser.UserAdmin', null=True, on_delete=models.SET_NULL)
    state_activite = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)
    start_date_activite = models.DateField()
    end_date_activite = models.DateField()
    price = models.IntegerField()
    photo = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Activite {self.id}"
