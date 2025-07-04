# Generated by Django 3.1.7 on 2021-04-05 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210402_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification_name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='qualification',
        ),
        migrations.AddField(
            model_name='profile',
            name='qualification',
            field=models.ManyToManyField(blank=True, max_length=100, to='accounts.Qualification'),
        ),
    ]
