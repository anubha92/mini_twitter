from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from core.models import UserProfileInfo, Tweets, Followers
from .forms import UserForm, UserProfileInfoForm, TweetsForm


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
    if request.method == 'POST':
        data = Followers.objects.filter(follow=User(u.user_id), user=request.user).count()
        if data == 0:
                if request.user != User(u.user_id):
                    f = Followers( follow=User(u.user_id), user=request.user)
                    f.save()
                else:
                    return HttpResponse("You cannot follow yourself")
        else:
            return HttpResponse("Already followed")
    return render(request, 'core/profile.html', {'profile_user':u, 'all_tweets':t})


def get_followers(request, pk):
    u = UserProfileInfo.objects.get(user_id=pk)
    follower = Followers.objects.filter(follow=User(u.user_id))
    return render(request, 'core/follower.html', {'all_followers':follower, 'profile_user':u})


def get_following(request, pk):
    u = UserProfileInfo.objects.get(user_id=pk)
    following = Followers.objects.filter(user=User(u.user_id))
    return render(request, 'core/following.html', {'all_following':following, 'profile_user':u })
