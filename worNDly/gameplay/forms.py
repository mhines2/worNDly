from django import forms

class GuessForm(forms.Form):
    guessed_string = forms.CharField(max_length=5, label='Your Guess')
