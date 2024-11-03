from django.shortcuts import render
import random
from .wordle import Guess, Solution
from .models import GamesPlayed
from django.contrib.auth.models import User
import datetime
from django.shortcuts import render
from store.models import GamesCounter


# Create your views here.

wordOfDay = ''




lang_files = {'gameplay/languages/en.txt': 'English',
              'gameplay/languages/de.txt': 'German',
              'gameplay/languages/es.txt': 'Spanish',
              'gameplay/languages/fr.txt': 'French',
              'gameplay/languages/pt.txt': 'Portuguese'
}

wordSet = {}
solution = ''
num_guesses = 0
guess_left = 6
found_word = False
yellow = []
gray = []
green = []
lang_file = ''
firstLet = ''
firstguess = 'XXXXX'
secondguess = 'XXXXX'
thirdguess = 'XXXXX'
fourthguess = 'XXXXX'
fifthguess = 'XXXXX'
lastguess = 'XXXXX'
gameEnded = False

allguesses = [['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray]
]

def desired_lang(request):
    if request.method == 'GET':
        return render(request, 'gameplay/choose_lang.html')
    else:
        print(request.POST)

def start_game(request, lang_file):
    max_plays = GamesCounter.objects.filter(player = request.user, todaysDate = datetime.date.today())[0].gamesForToday
    print('max_plays', max_plays)
    global wordOfDay
    global wordSet
    global solution
    global num_guesses
    global found_word
    global guess_left
    global green, gray, yellow
    global firstguess, secondguess, thirdguess, fourthguess, fifthguess, lastguess
    global allguesses
    global gameEnded
    global error_message

    if request.method == 'GET':
        gameEnded = False
        error_message = None

        num_guesses = 0
        wordSet = readWordSet(lang_file)
        print('word from', lang_file)
        wordOfDay = random.choice(list(wordSet))
        solution = Solution(wordOfDay, len(wordOfDay))
        print(wordOfDay, solution)
        guess_left = 6
        found_word = False
        yellow = []
        gray = []
        green = []
        allguesses = [['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray],
              ['XXXXX', green, yellow, gray]
                ]
        
        firstguess = 'XXXXX'
        secondguess = 'XXXXX'
        thirdguess = 'XXXXX'
        fourthguess = 'XXXXX'
        fifthguess = 'XXXXX'
        lastguess = 'XXXXX'

        numGamesPlayedThusFar = 0
        for game_played in GamesPlayed.objects.all():
            if request.user == game_played.player and game_played.game_play_date == datetime.date.today():
                numGamesPlayedThusFar += 1
            
        if numGamesPlayedThusFar >= max_plays:
            return render(request, 'gameplay/config_game.html', {
                'guesses_left': 'All plays used up!',
                'language_selected': lang_files[lang_file],
                'word_of_day': wordOfDay,
                'solution': solution,
                'yellow_letters': yellow,
                'gray_letters': gray,
                'green_letters': green,
                'firstguess': firstguess,
                'secondguess': secondguess,
                'thirdguess': thirdguess,
                'fourthguess': fourthguess,
                'fifthguess': fifthguess,
                'lastguess': lastguess,
                'allguesses': allguesses,
                'max_plays': max_plays,
                'numGamesPlayedThusFar': numGamesPlayedThusFar,
            })



    elif num_guesses < 6 and request.method == 'POST' and not found_word:
        numGamesPlayedThusFar = 0
        for game_played in GamesPlayed.objects.all():
            if request.user == game_played.player and game_played.game_play_date == datetime.date.today():
                numGamesPlayedThusFar += 1
            
        if numGamesPlayedThusFar >= max_plays:
            return render(request, 'gameplay/config_game.html', {
                'guesses_left': 'All plays used up!',
                'language_selected': lang_files[lang_file],
                'word_of_day': wordOfDay,
                'solution': solution,
                'yellow_letters': yellow,
                'gray_letters': gray,
                'green_letters': green,
                'firstguess': firstguess,
                'secondguess': secondguess,
                'thirdguess': thirdguess,
                'fourthguess': fourthguess,
                'fifthguess': fifthguess,
                'lastguess': lastguess,
                'allguesses': allguesses,
                'max_plays': max_plays, 
                'numGamesPlayedThusFar': numGamesPlayedThusFar, 
            })


        if request.POST['curr_guess'].upper() not in wordSet or len(request.POST['curr_guess']) != 5:
            error_message = 'Invalid word. Please enter a valid five-letter word.'
            print('Invalid word!', request.POST['curr_guess'])
            return render(request, 'gameplay/config_game.html', {
                'error_message': error_message,
                'guesses_left': guess_left,
                'language_selected': lang_files[lang_file],
                'word_of_day': wordOfDay,
                'solution': solution,
                'yellow_letters': yellow,
                'gray_letters': gray,
                'green_letters': green,
                'firstguess': firstguess,
                'secondguess': secondguess,
                'thirdguess': thirdguess,
                'fourthguess': fourthguess,
                'fifthguess': fifthguess,
                'lastguess': lastguess,
                'allguesses': allguesses,
                'max_plays': max_plays,
                'numGamesPlayedThusFar': numGamesPlayedThusFar,
            })

        num_guesses += 1
        print(request.POST)
        print('num_guesses', num_guesses)
        guessedString = request.POST['curr_guess']

        guess = Guess(guessedString, len(guessedString))
        if num_guesses == 1:
            firstguess = guess.string
        elif num_guesses == 2:
            secondguess = guess.string
        elif num_guesses == 3:
            thirdguess = guess.string
        elif num_guesses == 4:
            fourthguess = guess.string
        elif num_guesses == 5:
            fifthguess = guess.string
        elif num_guesses == 6:
            lastguess = guess.string

        guess_left -= 1
        yellow, gray, green = solution.evaluateLetters(guess.string)
        allguesses[num_guesses - 1] = [guess.string, green, yellow, gray]
        print(allguesses[num_guesses - 1])
        found_word = all(green)
        if found_word:
            print('WORD FOUND!')
            guess_left = f'Well done! You won in {num_guesses} guesses.'

        if found_word or num_guesses == 6:
            gameEnded = True


    elif num_guesses == 6:
        guess_left = 'NO GUESSES LEFT!'
        #gameEnded = True

    
    elif found_word:
        print('WORD FOUND!')
        guess_left = f'Well done! You won in {num_guesses} guesses.'
        #gameEnded = True
    
    if gameEnded:
        print('And now your game has ended')

        game = GamesPlayed(player = request.user, wordOfDayz = wordOfDay, won_or_nah = found_word,
                            num_guesses_that_occurred = num_guesses, game_play_date = datetime.date.today())

        
        print(game)
        print(game.player, game.num_guesses_that_occurred)
        game.save()

    # Render the config_game.html template with necessary context
    return render(request, 'gameplay/config_game.html', {
        'guesses_left': guess_left,
        'language_selected': lang_files[lang_file],
        'word_of_day': wordOfDay,
        'solution': solution,
        'yellow_letters': yellow,
        'gray_letters': gray,
        'green_letters': green,
        'firstguess': firstguess,
        'secondguess': secondguess,
        'thirdguess': thirdguess,
        'fourthguess': fourthguess,
        'fifthguess': fifthguess,
        'lastguess': lastguess,
        'allguesses': allguesses,
        'max_plays': max_plays,  
        'numGamesPlayedThusFar': numGamesPlayedThusFar,
    })

def start_game_GERMAN(request):
    return start_game(request, 'gameplay/languages/de.txt')

def start_game_SPANISH(request):
    return start_game(request, 'gameplay/languages/es.txt')

def start_game_PORT(request):
    return start_game(request, 'gameplay/languages/pt.txt')

def start_game_FRENCH(request):
    return start_game(request, 'gameplay/languages/fr.txt')

def start_game_ENGLISH(request):
    return start_game(request, 'gameplay/languages/en.txt')

def readWordSet(language):
    # Define file paths based on selected language
    return {word.strip().upper() for word in open(language)}