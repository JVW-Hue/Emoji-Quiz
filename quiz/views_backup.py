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
        # Get a quiz first
        quiz = Quiz.objects.order_by('?').first()
        if not quiz:
            return render(request, 'quiz/no_quizzes.html')
        
        # Default values
        user_score = 0
        games_remaining = "Unlimited"
        user_monthly_score = 0
        profile = None
        
        # Handle authenticated users
        if request.user.is_authenticated:
            try:
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                
                if not profile.can_play():
                    return render(request, 'quiz/limit_reached.html', {
                        'games_remaining': profile.games_remaining(),
                        'is_premium': profile.is_premium
                    })
                
                user_score = Score.objects.filter(user=request.user, correct=True).count()
                games_remaining = profile.games_remaining()
                
                try:
                    monthly_score = MonthlyScore.get_current_month_score(request.user)
                    user_monthly_score = monthly_score.total_score
                except:
                    user_monthly_score = 0
            except:
                pass  # Continue with defaults
        
        return render(request, 'quiz/home.html', {
            'quiz': quiz,
            'user_score': user_score,
            'games_remaining': games_remaining,
            'user_monthly_score': user_monthly_score
        })
    except Exception as e:
        # Simple fallback page
        return render(request, 'quiz/simple_home.html', {'error': str(e)})

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
    try:
        now = timezone.now()
        monthly_leaders = []
        all_time_leaders = []
        user_monthly_score = 0
        user_rewards = []
        
        try:
            monthly_leaders = MonthlyScore.objects.filter(
                month=now.month, year=now.year
            ).select_related('user').order_by('-total_score')[:10]
        except:
            pass
        
        try:
            all_time_leaders = User.objects.filter(score__correct=True).distinct().annotate(
                correct_count=Count('score', filter=Q(score__correct=True))
            ).order_by('-correct_count')[:10]
        except:
            pass
        
        if request.user.is_authenticated:
            try:
                monthly_score = MonthlyScore.get_current_month_score(request.user)
                user_monthly_score = monthly_score.total_score
            except:
                pass
            
            try:
                user_rewards = UserReward.objects.filter(
                    user=request.user, month=now.month, year=now.year
                ).select_related('reward')
            except:
                pass
        
        return render(request, 'quiz/leaderboard.html', {
            'monthly_leaders': monthly_leaders,
            'all_time_leaders': all_time_leaders,
            'user_monthly_score': user_monthly_score,
            'user_rewards': user_rewards,
            'current_month': now.strftime('%B %Y')
        })
    except:
        return render(request, 'quiz/simple_home.html', {'error': 'Leaderboard temporarily unavailable'})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username:
            return render(request, 'quiz/login.html', {'error': 'Please enter a username'})
        
        if password:  # Login with password
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'quiz/login.html', {'error': 'Invalid username or password'})
        else:  # Quick register without password
            try:
                if User.objects.filter(username=username).exists():
                    return render(request, 'quiz/login.html', {'error': 'Username taken. Try logging in or choose another name.'})
                
                # Create user with username as password for simplicity
                user = User.objects.create_user(username=username, password=username)
                user = authenticate(username=username, password=username)
                login(request, user)
                return redirect('home')
            except Exception as e:
                return render(request, 'quiz/login.html', {'error': 'Error creating account. Please try again.'})
    
    return render(request, 'quiz/login.html')

def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
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

@login_required
def user_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        try:
            monthly_score = MonthlyScore.get_current_month_score(request.user)
        except:
            monthly_score = type('obj', (object,), {'total_score': 0, 'games_played': 0})
        
        try:
            user_rewards = UserReward.objects.filter(
                user=request.user, 
                month=timezone.now().month, 
                year=timezone.now().year
            ).select_related('reward')
        except:
            user_rewards = []
        
        total_games = Score.objects.filter(user=request.user).count()
        correct_answers = Score.objects.filter(user=request.user, correct=True).count()
        accuracy = (correct_answers / total_games * 100) if total_games > 0 else 0
        
        return render(request, 'quiz/profile.html', {
            'profile': profile,
            'monthly_score': monthly_score,
            'user_rewards': user_rewards,
            'total_games': total_games,
            'correct_answers': correct_answers,
            'accuracy': round(accuracy, 1)
        })
    except Exception as e:
        return redirect('home')