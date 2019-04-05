from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'core'
# Be careful setting the name to just /login use userlogin instead!

urlpatterns=[
    path('register/',views.register,name='register'),
    path('home/', views.home, name='home'),
    path('home/tweet/', views.post_tweet, name='post_tweet'),
    path('home/tweet/like/<tweet_id>/', views.post_like, name='post_like'),
    path('profile/<userid>/', views.get_profile, name='get_profile'),
    path('profile/<userid>/followers/', views.get_followers, name='get_followers'),
    path('profile/<userid>/following/', views.get_following, name='get_following'),
    path('home/search/', views.search_profile, name='search_profile'),
    path('timeline/', views.timeline, name='timeline'),
    path('editbio/', views.edit_bio, name='edit_bio'),
    path('searchtweet/', views.search_tweet_full_text, name='search_tweet'),
]