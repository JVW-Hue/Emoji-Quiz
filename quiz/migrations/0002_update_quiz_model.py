# Generated migration to update Quiz model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='answer',
            new_name='option1',
        ),
        migrations.AddField(
            model_name='quiz',
            name='question',
            field=models.CharField(default='What movie does this represent?', max_length=200),
        ),
        migrations.AddField(
            model_name='quiz',
            name='option2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='quiz',
            name='option3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='quiz',
            name='option4',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='quiz',
            name='correct_index',
            field=models.IntegerField(default=0),
        ),
    ]