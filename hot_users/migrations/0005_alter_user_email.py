# Generated by Django 5.1.4 on 2025-01-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hot_users', '0004_alter_role_idrole_alter_role_poste_alter_user_iduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
