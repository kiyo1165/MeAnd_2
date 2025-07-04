# Generated by Django 3.1.7 on 2021-03-14 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_text', models.TextField(max_length=1000, verbose_name='メッセージ')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日付')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_user', to=settings.AUTH_USER_MODEL)),
                ('user_2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_user2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
