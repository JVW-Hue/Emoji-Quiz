from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check/<int:quiz_id>/', views.check_answer, name='check_answer'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('premium/', views.premium_upgrade, name='premium_upgrade'),
    path('buy-games/', views.buy_games, name='buy_games'),
    path('paypal/success/', views.paypal_success, name='paypal_success'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('paypal/debug/', views.paypal_debug, name='paypal_debug'),
]