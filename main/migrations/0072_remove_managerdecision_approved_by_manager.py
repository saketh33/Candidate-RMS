# Generated by Django 3.2.6 on 2023-12-05 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0071_alter_meetingschedule_scheduled_meet_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='managerdecision',
            name='approved_by_manager',
        ),
    ]