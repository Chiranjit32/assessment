# Generated by Django 4.1.3 on 2022-11-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_remove_ipmodel_end_ip_remove_ipmodel_start_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipmodel',
            name='end_ip',
            field=models.CharField(blank=True, max_length=39, null=True),
        ),
        migrations.AddField(
            model_name='ipmodel',
            name='start_ip',
            field=models.CharField(blank=True, max_length=39, null=True),
        ),
    ]
