# Generated by Django 4.1.3 on 2022-11-26 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_ipmodel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpDayCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
