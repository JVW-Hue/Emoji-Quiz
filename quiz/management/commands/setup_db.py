from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            self.stdout.write('Setting up database...')
            call_command('migrate')
            self.stdout.write('Loading sample quizzes...')
            call_command('load_sample_quizzes')
            self.stdout.write('Setting up rewards...')
            call_command('setup_rewards')
            self.stdout.write('Database setup complete!')
        except Exception as e:
            self.stdout.write(f'Setup error: {e}')
            self.stdout.write('Continuing with partial setup...')