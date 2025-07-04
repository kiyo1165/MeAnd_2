# Generated by Django 3.1.7 on 2021-04-07 06:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan', '0007_plan_style_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckOutList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strip_id', models.CharField(max_length=255, verbose_name='購入情報')),
                ('done_flag', models.BooleanField(default=False, verbose_name='カウンセリング完了フラグ')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 4, 7, 6, 34, 19, 787050, tzinfo=utc), verbose_name='契約日')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plan.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
