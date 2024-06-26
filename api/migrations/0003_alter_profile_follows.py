# Generated by Django 4.2.4 on 2023-12-04 07:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_alter_profile_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, null=True, related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
