# Generated by Django 5.0.3 on 2024-06-18 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0011_fight_f_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='amount',
            field=models.IntegerField(blank=True, max_length=100),
        ),
    ]