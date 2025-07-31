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
from .models import Quiz, Score, UserProfile, MonthlyScore, Reward, UserReward
import random

def home(request):
    try:
        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            if not profile.can_play():
                return render(request, 'quiz/limit_reached.html', {
                    'games_remaining': profile.games_remaining(),
                    'is_premium': profile.is_premium
                })
        
        quiz = Quiz.objects.order_by('?').first()
        if not quiz:
            # No quizzes available, redirect to setup
            return render(request, 'quiz/no_quizzes.html')
            
        user_score = 0
        games_remaining = "Unlimited"
        user_monthly_score = 0
        
        if request.user.is_authenticated:
            user_score = Score.objects.filter(user=request.user, correct=True).count()
            games_remaining = profile.games_remaining()
            monthly_score = MonthlyScore.get_current_month_score(request.user)
            user_monthly_score = monthly_score.total_score
        
        return render(request, 'quiz/home.html', {
            'quiz': quiz,
            'user_score': user_score,
            'games_remaining': games_remaining,
            'user_monthly_score': user_monthly_score
        })
    except Exception as e:
        return render(request, 'quiz/error.html', {'error': str(e)})

def check_answer(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        answer_index = int(request.POST.get('answer_index', -1))
        correct = answer_index == quiz.correct_index
        
        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Use a game
            profile.use_game()
            
            # Update regular score
            Score.objects.update_or_create(
                user=request.user, quiz=quiz,
                defaults={'correct': correct}
            )
            
            # Update monthly score
            monthly_score = MonthlyScore.get_current_month_score(request.user)
            monthly_score.games_played += 1
            if correct:
                monthly_score.total_score += 10  # 10 points per correct answer
            monthly_score.save()
            
            # Check for rewards
            check_and_award_rewards(request.user, monthly_score.total_score)
        
        return JsonResponse({
            'correct': correct,
            'correct_index': quiz.correct_index,
            'answer': quiz.correct_answer,
            'next_quiz_url': '/'
        })

def check_and_award_rewards(user, current_score):
    """Check if user earned any new rewards"""
    try:
        now = timezone.now()
        available_rewards = Reward.objects.filter(
            is_active=True,
            points_required__lte=current_score
        )
        
        for reward in available_rewards:
            user_reward, created = UserReward.objects.get_or_create(
                user=user, reward=reward, month=now.month, year=now.year
            )
            
            if created:
                # Apply reward
                profile, _ = UserProfile.objects.get_or_create(user=user)
                if reward.reward_type == 'extra_games':
                    profile.extra_games += reward.reward_value
                    profile.save()
                elif reward.reward_type == 'premium_days':
                    if profile.premium_expires:
                        profile.premium_expires += timedelta(days=reward.reward_value)
                    else:
                        profile.premium_expires = timezone.now() + timedelta(days=reward.reward_value)
                        profile.is_premium = True
                    profile.save()
    except Exception:
        pass  # Silently fail to avoid breaking the game

def leaderboard(request):
    now = timezone.now()
    
    # Get current month leaderboard
    monthly_leaders = MonthlyScore.objects.filter(
        month=now.month, year=now.year
    ).select_related('user').order_by('-total_score')[:10]
    
    # Get all-time leaderboard
    all_time_leaders = User.objects.filter(score__correct=True).distinct().annotate(
        correct_count=Count('score', filter=Q(score__correct=True))
    ).order_by('-correct_count')[:10]
    
    user_monthly_score = 0
    user_rewards = []
    
    if request.user.is_authenticated:
        monthly_score = MonthlyScore.get_current_month_score(request.user)
        user_monthly_score = monthly_score.total_score
        
        # Get user's rewards for this month
        user_rewards = UserReward.objects.filter(
            user=request.user, month=now.month, year=now.year
        ).select_related('reward')
    
    return render(request, 'quiz/leaderboard.html', {
        'monthly_leaders': monthly_leaders,
        'all_time_leaders': all_time_leaders,
        'user_monthly_score': user_monthly_score,
        'user_rewards': user_rewards,
        'current_month': now.strftime('%B %Y')
    })

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
            profile.premium_expires = timezone.now() + timedelta(days=30)
            profile.save()
            message = "Premium upgrade successful! You now have unlimited games for 30 days."
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