# Generated by Django 5.1.7 on 2025-05-08 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Artists', '0004_alter_artworksubmission_reviewed_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artworksubmission',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
