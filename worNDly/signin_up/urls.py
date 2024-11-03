from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_users, name="login"),
    path('logout/', views.logout_users, name='logout'),
    path('create/', views.create_new_user, name="create"),
    path('', views.homepage, name="homepage"),
]