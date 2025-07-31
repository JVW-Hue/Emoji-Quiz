# Emoji Quiz Django App

A minimal Django web app where users guess movies from emoji sequences.

## Setup

1. Install Django: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Load sample quizzes: `python manage.py load_sample_quizzes`
4. Create admin user: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## Features

- Random emoji quiz display
- Quick username login
- Score tracking
- Leaderboard
- Admin interface for adding quizzes

## Usage

Visit http://127.0.0.1:8000/ to start playing!