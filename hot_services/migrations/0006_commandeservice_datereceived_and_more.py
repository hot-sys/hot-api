# Generated by Django 5.1.4 on 2025-01-15 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hot_clients', '0003_alter_client_idclient'),
        ('hot_services', '0005_alter_service_idservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandeservice',
            name='dateReceived',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='commandeservice',
            name='idCommandeCommune',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='commandeservice',
            name='received',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='commandeservice',
            name='idClient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hot_clients.client'),
        ),
    ]
