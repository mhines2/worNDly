from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wallet(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.player.username

class GamesCounter(models.Model):
    gamesForToday = models.IntegerField(default = 3)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    todaysDate = models.DateField()

    def __str__(self):
        return f'{self.player} has {self.gamesForToday} games for {self.todaysDate}.'