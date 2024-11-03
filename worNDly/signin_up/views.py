from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import GamesCounter
import datetime

def homepage(request):
    return render(request, 'signin_up/homepage.html')

# Feature 1.1: Create User
def create_new_user(request):
    if request.method == 'GET':
        return render(request, 'signin_up/sign_in.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'signin_up/sign_in.html')
        
        # Create user
        new_user = User.objects.create_user(username=username, email=email, password=password)
        
        # Print user information
        print("New User Created:")
        print("Username:", new_user.username)
        print("Email:", new_user.email)
            
        messages.success(request, 'User created successfully. Please log in.')
        return redirect('/')
    
# Feature 1.2: Sign-in
def login_users(request):
    if request.method == 'GET':
        return render(request, 'signin_up/login_user.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username and password are provided
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'signin_up/login_user.html')

        # Authenticate user
        user = authenticate(username=username, password=password)
        
        # Debug print
        print("Signing in...")
        print("Username:", username)
        # print("Password:", password)
        if user:
            print("Authenticated User: True")
        else:
            print("Authenticated User: False")
        
        
        # Check if authentication failed
        if user is not None:
            # Authentication successful
            login(request, user)
            new_user = True
            new_name = user.username
            # Redirect to homepage
            
            
            if GamesCounter.objects.filter(player=user, todaysDate=datetime.date.today()).exists():
                print('Already in db.')
            else:
                personPlays = GamesCounter(player = user, todaysDate = datetime.date.today())
                personPlays.save()

                print(personPlays)
            return render(request, 'homepage.html', {'new_user': new_user, 'new_name': new_name})
        else: 
            messages.error(request, 'Invalid username or password.')
            return render(request, 'signin_up/login_user.html')

# Feature 1.3: Sign-out
def logout_users(request):
    print(f'Signing out...')
    logout(request)
    return redirect('/')


