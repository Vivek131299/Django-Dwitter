# Generated by Django 4.2.4 on 2023-12-12 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='dweet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dweet_likes', to='api.dweet'),
        ),
        migrations.AlterField(
            model_name='like',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_likes', to='api.profile'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dweet_comments', to='api.dweet')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_comments', to='api.profile')),
            ],
        ),
    ]
