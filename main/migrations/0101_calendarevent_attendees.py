# Generated by Django 3.2.6 on 2024-01-03 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0100_calendarevent_unique_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='attendees',
            field=models.TextField(blank=True, null=True),
        ),
    ]