# Generated by Django 5.0.3 on 2024-08-13 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0015_commissionrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='fightno',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bet',
            name='longest',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bet',
            name='winStat',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='bet',
            name='winning_amnt',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='bet',
            name='won_amnt',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='fight',
            name='f_tblrows',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='games',
            name='g_col',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='userwallet',
            name='commission_rate',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='userwallet',
            name='default_rate',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=5),
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('c_player', models.CharField(max_length=100)),
                ('c_agent', models.CharField(default='', max_length=100)),
                ('c_fnumber', models.CharField(default=0, max_length=50)),
                ('c_betamnt', models.CharField(max_length=50)),
                ('c_winner', models.CharField(max_length=50)),
                ('c_commission', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('c_fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commissions', to='ugs_app.fight')),
            ],
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('p_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('p_code', models.CharField(blank=True, max_length=50, null=True)),
                ('p_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('p_created', models.DateTimeField(auto_now_add=True)),
                ('p_update', models.DateTimeField(auto_now=True)),
                ('p_sellerUkey', models.CharField(blank=True, max_length=100, null=True)),
                ('p_receiver', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='p_userkey', to=settings.AUTH_USER_MODEL)),
                ('p_sender', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='p_headKey', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UWalletCashout',
            fields=[
                ('cw_id', models.AutoField(primary_key=True, serialize=False)),
                ('cw_code', models.CharField(blank=True, max_length=50, null=True)),
                ('cw_bal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cw_out', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cw_remaining', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cw_update', models.DateTimeField(auto_now=True)),
                ('cw_created', models.DateTimeField(auto_now_add=True)),
                ('cw_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cw_player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CommissionRate',
        ),
    ]