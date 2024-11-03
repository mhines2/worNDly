# views.py

from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.models import User
from .models import GamesCounter
import datetime

class BuyGamePlaysForm(forms.Form):
    num_plays = forms.IntegerField(label='Number of game plays to purchase (number > 1)')

    
def view_balance(access_token, email):
   # Use the access token to make an authenticated request
   headers = {'Authorization': f'Bearer {access_token}'}
   # Make a GET request with the authorization header
   api_response = requests.get(f"https://jcssantos.pythonanywhere.com/api/group10/group10/player/{email}/", headers=headers)
   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()['amount']
   else:
       print("Failed to access the API endpoint to view balance for user:", api_response.status_code)

def buy_game_plays(access_token, email, num_plays):
    current_balance = view_balance(access_token, email)
    print(current_balance)
    cost = num_plays
    if current_balance >= cost:
        url = f"https://jcssantos.pythonanywhere.com/api/group10/group10/player/{email}/pay"
        data = {"amount": cost}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            new_balance = response.json()["new_amount"]
            the_user = User.objects.filter(email = email)[0]
            the_gamePlayed = GamesCounter.objects.filter(player = the_user, todaysDate = datetime.date.today())[0]
            the_gamePlayed.gamesForToday += num_plays
            print(the_gamePlayed)
            the_gamePlayed.save()


             
            return f"Successfully purchased {num_plays} extra game plays. New coin balance: {new_balance}"
        else:
            return response.json()["message"]  # Error message from API
    else:
        return "Insufficient funds to purchase game plays"

@login_required
def purchase_games(request):
    email = request.user.email
    access_token = API_KEY # Replace with your API key
    if request.method == 'GET':
        num_games = view_balance(access_token, email)  # Retrieve balance directly
        print(num_games)
        if num_games is not None:  # Ensure num_games is not None
            return render(request, 'store/purchase_games.html', {
                'num_games': num_games  # Pass the balance value to the template
            })
    
    if request.method == 'POST':
        form = BuyGamePlaysForm(request.POST)
        if form.is_valid():
            num_plays = form.cleaned_data['num_plays']
            response = buy_game_plays(access_token, email, num_plays)
            return render(request, 'store/purchase_games.html', {'form': form, 'response': response}) # Pass the form back to the template
    else:
        form = BuyGamePlaysForm()
    return render(request, 'store/purchase_games.html', {'form': form})


