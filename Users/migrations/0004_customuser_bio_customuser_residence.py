# Generated by Django 5.1.7 on 2025-03-17 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='residence',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
