# Generated by Django 5.1.6 on 2025-07-30 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_update_quiz_model'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='option1',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_played_today', models.IntegerField(default=0)),
                ('last_game_date', models.DateField(auto_now_add=True)),
                ('is_premium', models.BooleanField(default=False)),
                ('premium_expires', models.DateTimeField(blank=True, null=True)),
                ('extra_games', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
