from django.contrib import admin
from .models import Quiz, Score

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['emojis', 'correct_answer', 'category']
    list_filter = ['category']

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'correct', 'timestamp']
    list_filter = ['correct', 'timestamp']