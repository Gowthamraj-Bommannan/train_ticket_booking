# Generated by Django 5.2.3 on 2025-07-01 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0002_alter_train_from_station_alter_train_to_station'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trainstation',
            unique_together=set(),
        ),
    ]
