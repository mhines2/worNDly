from django.shortcuts import render
from django.contrib.auth.models import User
from gameplay.models import GamesPlayed
import datetime

def open_dashboard(request):
    #get the plays statistics for the player:
    selected_data_view = request.GET.get('data-view', 'all')  # Get selected data view from the form

    listOfPlays = []
    listOfPlaysYEAR = []
    listOfPlaysMONTH = []
    listOfPlaysWEEK = []
    for g in GamesPlayed.objects.all():
        if request.user == g.player:
            listOfPlays.append(g)
        
        if request.user == g.player and g.game_play_date.year == datetime.datetime.now().year:
            listOfPlaysYEAR.append(g)
        
        if request.user == g.player and g.game_play_date.month == datetime.datetime.now().month:
            listOfPlaysMONTH.append(g)
        
        if request.user == g.player and g.game_play_date.isocalendar()[1] == datetime.datetime.now().isocalendar()[1]:
            listOfPlaysWEEK.append(g)

    #get the percentages and guesses distribution:
    tot = 0
    succ = 0
    perc = 0
    guess_stats = [0,0,0,0,0,0]
    for g in GamesPlayed.objects.filter(player = request.user):
        tot += 1
        if g.won_or_nah:
            succ += 1
            guess_stats[g.num_guesses_that_occurred-1] +=1
        
    if tot:
        perc = round((succ / tot) * 100, 1)
    # Pass the selected data view and relevant data to the template
    return render(request, 'dashboard/firstdash.html', {
        'selected_data_view': selected_data_view,
        'listOfPlays': listOfPlays,
        'listOfPlaysYEAR': listOfPlaysYEAR,
        'listOfPlaysMONTH': listOfPlaysMONTH,
        'listOfPlaysWEEK': listOfPlaysWEEK,
        'tot': tot, 
        'perc': str(perc) + '%', 
        'guess_stats': guess_stats
    })