# Generated by Django 3.1.7 on 2021-04-22 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0007_plan_style_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(blank=True, max_length=20)),
                ('pref', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='plan.pref')),
            ],
        ),
    ]
