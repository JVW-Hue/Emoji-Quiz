from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import calendar

class Quiz(models.Model):
    emojis = models.CharField(max_length=200)
    question = models.CharField(max_length=200, default='What movie does this represent?')
    option1 = models.CharField(max_length=100, default='')
    option2 = models.CharField(max_length=100, default='')
    option3 = models.CharField(max_length=100, default='')
    option4 = models.CharField(max_length=100, default='')
    correct_index = models.IntegerField(default=0)  # 0-3 for options 1-4
    category = models.CharField(max_length=50, default='movie')
    
    @property
    def options(self):
        return [self.option1, self.option2, self.option3, self.option4]
    
    @property
    def correct_answer(self):
        return self.options[self.correct_index]
    
    def __str__(self):
        return f"{self.emojis} - {self.correct_answer}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games_played_today = models.IntegerField(default=0)
    last_game_date = models.DateField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    premium_expires = models.DateTimeField(null=True, blank=True)
    extra_games = models.IntegerField(default=0)
    
    def can_play(self):
        today = timezone.now().date()
        if self.last_game_date != today:
            self.games_played_today = 0
            self.last_game_date = today
            self.save()
        
        if self.is_premium and (not self.premium_expires or timezone.now() < self.premium_expires):
            return True
        
        if self.extra_games > 0:
            return True
            
        return self.games_played_today < 30
    
    def use_game(self):
        if self.extra_games > 0:
            self.extra_games -= 1
        else:
            self.games_played_today += 1
        self.save()
    
    def games_remaining(self):
        if self.is_premium and (not self.premium_expires or timezone.now() < self.premium_expires):
            return "Unlimited"
        
        if self.extra_games > 0:
            return self.extra_games + (30 - self.games_played_today)
        
        return max(0, 30 - self.games_played_today)

class MonthlyScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'month', 'year']
    
    @classmethod
    def get_current_month_score(cls, user):
        now = timezone.now()
        score, created = cls.objects.get_or_create(
            user=user, month=now.month, year=now.year,
            defaults={'total_score': 0, 'games_played': 0}
        )
        return score

class Reward(models.Model):
    REWARD_TYPES = [
        ('badge', 'Badge'),
        ('extra_games', 'Extra Games'),
        ('premium_days', 'Premium Days'),
        ('title', 'Special Title'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    reward_value = models.IntegerField(default=0)
    points_required = models.IntegerField()
    emoji = models.CharField(max_length=10, default='🏆')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.emoji} {self.name} ({self.points_required} points)"

class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField()
    year = models.IntegerField()
    
    class Meta:
        unique_together = ['user', 'reward', 'month', 'year']

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'quiz']