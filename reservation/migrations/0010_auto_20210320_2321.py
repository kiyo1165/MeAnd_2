# Generated by Django 3.1.7 on 2021-03-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0009_reservation_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='active',
            field=models.BooleanField(default=True, verbose_name='稼働可否'),
        ),
    ]
