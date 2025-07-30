from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from .models import Quiz, Score, UserProfile
import random

def home(request):
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if not profile.can_play():
            return render(request, 'quiz/limit_reached.html', {
                'games_remaining': profile.games_remaining(),
                'is_premium': profile.is_premium
            })
    
    quiz = Quiz.objects.order_by('?').first()
    user_score = 0
    games_remaining = "Unlimited"
    
    if request.user.is_authenticated:
        user_score = Score.objects.filter(user=request.user, correct=True).count()
        games_remaining = profile.games_remaining()
    
    return render(request, 'quiz/home.html', {
        'quiz': quiz,
        'user_score': user_score,
        'games_remaining': games_remaining
    })

def check_answer(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        answer_index = int(request.POST.get('answer_index', -1))
        correct = answer_index == quiz.correct_index
        
        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Use a game
            profile.use_game()
            
            Score.objects.update_or_create(
                user=request.user, quiz=quiz,
                defaults={'correct': correct}
            )
        
        return JsonResponse({
            'correct': correct,
            'correct_index': quiz.correct_index,
            'answer': quiz.correct_answer,
            'next_quiz_url': '/'
        })

def leaderboard(request):
    if request.user.is_authenticated:
        user_score = Score.objects.filter(user=request.user, correct=True).count()
        top_users = User.objects.filter(score__correct=True).distinct().annotate(
            correct_count=Count('score', filter=Q(score__correct=True))
        ).order_by('-correct_count')[:10]
        return render(request, 'quiz/leaderboard.html', {
            'user_score': user_score,
            'top_users': top_users
        })
    return redirect('home')

def quick_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user, created = User.objects.get_or_create(username=username)
        login(request, user)
    return redirect('home')

@login_required
def premium_upgrade(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'quiz/premium.html', {'profile': profile})

@login_required
def buy_games(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'quiz/buy_games.html', {'profile': profile})

@login_required
def paypal_success(request):
    try:
        payment_type = request.GET.get('type', 'premium')
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if payment_type == 'premium':
            profile.is_premium = True
            profile.premium_expires = timezone.now() + timedelta(days=365)
            profile.save()
            message = "Premium upgrade successful! You now have unlimited games."
        else:
            profile.extra_games += 30
            profile.save()
            message = "Purchase successful! You now have 30 additional games."
        
        return render(request, 'quiz/payment_success.html', {'message': message})
    except Exception as e:
        return render(request, 'quiz/payment_cancel.html', {'error': str(e)})

@login_required
def paypal_cancel(request):
    return render(request, 'quiz/payment_cancel.html')

def paypal_debug(request):
    return render(request, 'quiz/paypal_debug.html')