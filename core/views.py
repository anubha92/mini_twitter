from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required



from core.models import User, Tweet, FollowRelation, UserProfileInfo
from .forms import UserForm, User, UserProfileInfoForm


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
    u = request.user
    if request.method == 'POST':
        new_tweet = request.POST.get('submit_tweet')
        t = Tweet.objects.create(contents=new_tweet, user=u)
        tweets_all = u.tweets.all()
        return render(request, 'core/mytweets1.html',{'tweets_all':tweets_all})
    else:
        tweets_all = u.tweets.all()
        return render(request, 'core/mytweets1.html',{'tweets_all':tweets_all})




def search_profile(request):
    user_list = UserProfileInfo.objects.all()
    return render(request, 'core/search.html', {'user_list': user_list})


def get_profile(request, pk):
    followed = False
    u = UserProfileInfo.objects.get(user_id=pk)
    t = Tweet.objects.filter(user_id=pk)
    if request.method == 'POST':
        data = FollowRelation.objects.filter(follow=User(u.user_id), user=request.user).count()
        if data == 0:
                if request.user != User(u.user_id):
                    f = FollowRelation( follow=User(u.user_id), user=request.user)
                    f.save()
                    followed = True
                else:
                    return HttpResponse("You cannot follow yourself")
        else:
            return HttpResponse("Already followed")
    return render(request, 'core/profile.html', {'profile_user':u, 'all_tweets':t, 'followed':followed})


def get_followers(request, pk):
    user_profile = UserProfileInfo.objects.get(user_id=pk)
    u = User.objects.get(username=user_profile.user.username)
    return render(request, 'core/follower.html', {'all_followers':u.followed.all(), 'profile_user':u})


def get_following(request,pk):
    user_profile = UserProfileInfo.objects.get(user_id=pk)
    u = User.objects.get(username=user_profile.user.username)
    return render(request, 'core/following.html', {'all_following':u.following.all(), 'profile_user':user_profile })


def timeline(request):
    u=request.user
    my_tweets = u.tweets.filter(user=u)
    following = u.following.all()
    for f in following:
        f_tweets = Tweet.objects.filter(user=f.follow)
        my_tweets = my_tweets | f_tweets
    return render(request, 'core/timeline.html',{'my_tweets': my_tweets})


def edit_bio(request):
    if request.method == 'POST':
        u = request.user
        updated_bio = request.POST.get('updated_bio')
        b = UserProfileInfo.objects.get(user=u)
        b.bio = updated_bio
        b.save()
        return HttpResponse("Bio has been updated")
    else:
        return render(request, 'core/edit_bio.html', {})


