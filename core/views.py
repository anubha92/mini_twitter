from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import escape

from core.models import UserProfileInfo, Tweets
from .forms import UserForm, UserProfileInfoForm, TweetsForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

# Create your views here.

def index(request):
    return render(request, 'core/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'core/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

'''
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            user_pref = UserProfileInfo.objects.get(user=user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'core/login.html', {})'''

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            user_pref = UserProfileInfo.objects.get(user=user)
            return render(request, 'core/home.html', {'bio': user_pref.bio})
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'core/login.html', {})

def post_tweet(request):
    tweeted = False
    tweet_form = TweetsForm(data=request.POST)
    user=request.user
    if request.method == 'POST':
        if tweet_form.is_valid():
            tweet = tweet_form.save(commit=False)
            tweet.user = user
            tweet.save()
            tweeted = True
        else:
            print("Tweetform invalid")
    else:
        tweet_form = TweetsForm()
    tweets_all = Tweets.objects.filter(user=user).order_by('-published_time')
    return render(request, 'core/mytweets.html',
                  {'tweet_form': tweet_form,
                   'tweets_all' : tweets_all,
                   'tweeted': tweeted})


def search_profile(request):
    user_list = UserProfileInfo.objects.all()
    return render(request, 'core/search.html', {'user_list': user_list})

def get_profile(request, pk):
    u = UserProfileInfo.objects.get(user_id=pk)
    t = Tweets.objects.filter(user_id=pk).order_by('-published_time')
    return render(request, 'core/profile.html', {'profile_user':u, 'all_tweets':t})
