from django.db import models

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    activite = models.ForeignKey('activity.Activite', on_delete=models.CASCADE)
    client = models.ForeignKey('clients.UserClient', on_delete=models.CASCADE)
    admin = models.ForeignKey('adminuser.UserAdmin', null=True, on_delete=models.SET_NULL)
    state = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    start_date_reservation = models.DateField()
    end_date_reservation = models.DateField()
    payment = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation {self.id}"
