from django.conf.urls import url
from core import views
from django.urls import path
# SET THE NAMESPACE!
app_name = 'core'
# Be careful setting the name to just /login use userlogin instead!

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^home/$', views.home, name='home'),
   # url(r'^home/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^home/tweet/$', views.post_tweet, name='post_tweet'),
    url(r'^profile/(?P<pk>[\w\-]+)/$', views.get_profile, name='get_profile'),
    url(r'^profile/(?P<pk>[\w\-]+)/followers/$', views.get_followers, name='get_followers'),
    url(r'^profile/(?P<pk>[\w\-]+)/following/$', views.get_following, name='get_following'),
    url(r'^home/search/$', views.search_profile, name='search_profile')
]