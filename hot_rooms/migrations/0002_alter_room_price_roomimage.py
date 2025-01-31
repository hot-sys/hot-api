# Generated by Django 4.1.13 on 2024-12-14 08:21

from django.db import migrations, models
import django.db.models.deletion
import hot_rooms.validators.price


class Migration(migrations.Migration):

    dependencies = [
        ('hot_rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price',
            field=models.IntegerField(validators=[hot_rooms.validators.price.validate_positive]),
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('idImage', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.URLField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('idRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='hot_rooms.room')),
            ],
        ),
    ]
