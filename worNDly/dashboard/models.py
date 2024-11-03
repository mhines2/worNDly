from django.db import models

# Create your models here.

'''class Past_Game(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateTimeField('date played')
    fail = models.BooleanField()
    attempts = models.IntegerField(max_length=6)

class Total_Games(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    total = models.IntegerField()
    wins = models.IntegerField()
    guess_tracker = ArrayField(
        models.IntegerField()
        size=6 #id if this is zero index or not
    )'''
