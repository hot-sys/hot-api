# Generated by Django 5.1.4 on 2025-01-21 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hot_rooms', '0008_commanderoom_datefreed_commanderoom_refund'),
    ]

    operations = [
        migrations.AddField(
            model_name='commanderoom',
            name='DateSupposed',
            field=models.DateTimeField(null=True),
        ),
    ]
