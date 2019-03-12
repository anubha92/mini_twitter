from django.conf.urls import url
from django.urls import path
from core import views

# SET THE NAMESPACE!
app_name = 'core'
# Be careful setting the name to just /login use userlogin instead!

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/tweet/$', views.post_tweet, name='post_tweet'),
    path('home/tweet/like/<tweet_id>/', views.post_like, name='post_like'),
    path('profile/<userid>/', views.get_profile, name='get_profile'),
    path('profile/<userid>/followers/', views.get_followers, name='get_followers'),
    path('profile/<userid>/following/', views.get_following, name='get_following'),
    url(r'^home/search/$', views.search_profile, name='search_profile'),
    url(r'^timeline/$', views.timeline, name='timeline'),
    url(r'^editbio/$', views.edit_bio, name='edit_bio'),
]