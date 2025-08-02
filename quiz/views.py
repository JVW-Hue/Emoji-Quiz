from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Quiz, Score, UserProfile, MonthlyScore
import random

def home(request):
    # Get a random quiz
    quiz = Quiz.objects.order_by('?').first()
    
    # Default values
    user_score = 0
    games_remaining = "Unlimited"
    
    # If user is logged in, get their data
    if request.user.is_authenticated:
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_score = Score.objects.filter(user=request.user, correct=True).count()
            games_remaining = profile.games_remaining()
            
            # Check if user can play
            if not profile.can_play():
                return render(request, 'quiz/limit_reached.html', {
                    'games_remaining': games_remaining,
                    'is_premium': profile.is_premium
                })
        except:
            pass
    
    return render(request, 'quiz/home.html', {
        'quiz': quiz,
        'user_score': user_score,
        'games_remaining': games_remaining,
        'user_monthly_score': 0
    })

def check_answer(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        answer_index = int(request.POST.get('answer_index', -1))
        correct = answer_index == quiz.correct_index
        
        if request.user.is_authenticated:
            try:
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                profile.use_game()
                
                Score.objects.update_or_create(
                    user=request.user, quiz=quiz,
                    defaults={'correct': correct}
                )
                
                # Update monthly score
                now = timezone.now()
                monthly_score, created = MonthlyScore.objects.get_or_create(
                    user=request.user, month=now.month, year=now.year,
                    defaults={'total_score': 0, 'games_played': 0}
                )
                monthly_score.games_played += 1
                if correct:
                    monthly_score.total_score += 10  # 10 points per correct answer
                monthly_score.save()
            except:
                pass
        
        return JsonResponse({
            'correct': correct,
            'correct_index': quiz.correct_index,
            'answer': quiz.correct_answer,
            'next_quiz_url': '/'
        })

def leaderboard(request):
    try:
        now = timezone.now()
        
        # Monthly leaderboard (resets each month)
        monthly_leaders = MonthlyScore.objects.filter(
            month=now.month, year=now.year
        ).select_related('user').order_by('-total_score')[:10]
        
        user_monthly_score = 0
        user_rank = 0
        
        if request.user.is_authenticated:
            try:
                monthly_score = MonthlyScore.objects.get(
                    user=request.user, month=now.month, year=now.year
                )
                user_monthly_score = monthly_score.total_score
                
                # Calculate user's rank this month
                better_scores = MonthlyScore.objects.filter(
                    month=now.month, year=now.year,
                    total_score__gt=user_monthly_score
                ).count()
                user_rank = better_scores + 1
            except:
                pass
        
        return render(request, 'quiz/leaderboard_monthly.html', {
            'monthly_leaders': monthly_leaders,
            'user_monthly_score': user_monthly_score,
            'user_rank': user_rank,
            'current_month': now.strftime('%B %Y')
        })
    except:
        return render(request, 'quiz/simple_home.html', {'error': 'Leaderboard error'})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username:
            return render(request, 'quiz/login.html', {'error': 'Please enter a username'})
        
        if password:  # Login
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # Make login permanent
                request.session.set_expiry(86400 * 365 * 10)  # 10 years
                return redirect('home')
            else:
                return render(request, 'quiz/login.html', {'error': 'Invalid login'})
        else:  # Register
            if User.objects.filter(username=username).exists():
                return render(request, 'quiz/login.html', {'error': 'Username taken'})
            
            user = User.objects.create_user(username=username, password=username)
            user = authenticate(username=username, password=username)
            login(request, user)
            # Make login permanent
            request.session.set_expiry(86400 * 365 * 10)  # 10 years
            return redirect('home')
    
    return render(request, 'quiz/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        total_games = Score.objects.filter(user=request.user).count()
        correct_answers = Score.objects.filter(user=request.user, correct=True).count()
        
        return render(request, 'quiz/profile_simple.html', {
            'profile': profile,
            'total_games': total_games,
            'correct_answers': correct_answers
        })
    except:
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
            message = "Premium upgrade successful!"
        else:
            profile.extra_games += 30
            profile.save()
            message = "Purchase successful!"
        
        return render(request, 'quiz/payment_success.html', {'message': message})
    except:
        return render(request, 'quiz/payment_cancel.html')

@login_required
def paypal_cancel(request):
    return render(request, 'quiz/payment_cancel.html')

def paypal_debug(request):
    return render(request, 'quiz/paypal_debug.html')