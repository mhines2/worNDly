# urls.py

from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('purchase/', views.purchase_games, name='purchase_games'),
    # Other URL patterns go here
]
