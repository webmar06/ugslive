# Generated by Django 5.0.3 on 2024-08-15 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0032_longestfight_l_dateclaimed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='longestfight',
            name='l_dateclaimed',
        ),
    ]