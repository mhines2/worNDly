# Generated by Django 4.2.6 on 2024-05-01 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GamesPlayed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordOfDayz', models.CharField(max_length=30)),
                ('won_or_nah', models.BooleanField()),
                ('num_guesses_that_occurred', models.IntegerField()),
                ('game_play_date', models.DateField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
