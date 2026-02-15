from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('comment/', views.comment, name='comment'),
    path('search/', views.search, name='search'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('liked-post/<uuid:postid>/', views.liked_post, name='likedpost'),
 
 
]