from django.core.management.base import BaseCommand
from quiz.models import Reward

class Command(BaseCommand):
    def handle(self, *args, **options):
        rewards = [
            # Student-friendly rewards
            ("🌟 First Steps", "Welcome reward for new players!", "extra_games", 5, 50, "🌟"),
            ("📚 Study Buddy", "You're getting the hang of this!", "badge", 0, 100, "📚"),
            ("🎯 Sharp Shooter", "Great accuracy in movie knowledge!", "extra_games", 10, 150, "🎯"),
            ("🧠 Movie Genius", "Your movie knowledge is impressive!", "premium_days", 3, 200, "🧠"),
            ("🏆 Quiz Master", "You've mastered the art of movie trivia!", "extra_games", 20, 300, "🏆"),
            ("👑 Movie King/Queen", "Bow down to the movie royalty!", "premium_days", 7, 500, "👑"),
            ("🎬 Hollywood Expert", "You know movies like a pro!", "extra_games", 30, 750, "🎬"),
            ("⭐ Legendary Player", "Your skills are legendary!", "premium_days", 14, 1000, "⭐"),
        ]
        
        created_count = 0
        for name, desc, reward_type, value, points, emoji in rewards:
            try:
                Reward.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': desc,
                        'reward_type': reward_type,
                        'reward_value': value,
                        'points_required': points,
                        'emoji': emoji,
                        'is_active': True
                    }
                )
                created_count += 1
            except Exception as e:
                continue
        
        self.stdout.write(f"Created {created_count} student-friendly rewards!")