# Generated by Django 5.0.3 on 2024-08-15 06:52

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0019_alter_fight_f_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Longestfight',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('l_amount', models.IntegerField(blank=True)),
                ('l_won_amnt', models.CharField(default=0, max_length=100)),
                ('l_category', models.CharField(choices=[('LONGEST', 'LONGEST')], max_length=50, null=True)),
                ('l_status', models.CharField(choices=[('WAITING', 'WAITING'), ('CLAIMED', 'CLAIMED')], default='WAITING', max_length=50)),
                ('l_fightno', models.IntegerField(default=0)),
                ('l_created', models.DateTimeField(auto_now_add=True)),
                ('l_fight', models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, related_name='l_fight', to='ugs_app.fight')),
                ('l_player', models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, related_name='l_player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]