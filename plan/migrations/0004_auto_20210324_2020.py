# Generated by Django 3.1.7 on 2021-03-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_auto_20210324_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='counseling_active',
            field=models.CharField(blank=True, choices=[('1', 'すぐに話せます。'), ('2', '本日中にお話ができます。'), ('2', '調整できます。')], max_length=20, verbose_name='カウンセリングのタイミング'),
        ),
    ]
