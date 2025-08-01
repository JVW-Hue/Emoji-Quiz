# Generated by Django 5.1.6 on 2025-07-31 19:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_quiz_option1_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('reward_type', models.CharField(choices=[('badge', 'Badge'), ('extra_games', 'Extra Games'), ('premium_days', 'Premium Days'), ('title', 'Special Title')], max_length=20)),
                ('reward_value', models.IntegerField(default=0)),
                ('points_required', models.IntegerField()),
                ('emoji', models.CharField(default='🏆', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('total_score', models.IntegerField(default=0)),
                ('games_played', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'month', 'year')},
            },
        ),
        migrations.CreateModel(
            name='UserReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'reward', 'month', 'year')},
            },
        ),
    ]
