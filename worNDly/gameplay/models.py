from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class GamesPlayed(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    wordOfDayz = models.CharField(max_length=30)
    won_or_nah = models.BooleanField() # Pass/fail
    num_guesses_that_occurred = models.IntegerField() # Number of guesses
    game_play_date = models.DateField() # Date field

    def __str__(self):
        if self.won_or_nah:
            str_to_add = 'PASS'
        else:
            str_to_add = 'FAIL'
        return f'{self.player}, on {self.game_play_date}: {str_to_add} in {self.num_guesses_that_occurred} for {self.wordOfDayz}'
    
