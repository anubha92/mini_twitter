from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError
from django.core.paginator import Paginator

from core.models import Tweet, FollowRelation, UserProfileInfo, TweetLike
from core.forms import User, UserCreationForm


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
        user_form = UserCreationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
            bio = user_form.cleaned_data.get('bio')
            profile_pic = user_form.cleaned_data.get('profile_pic')
            profile = UserProfileInfo(user=user, bio=bio, profile_pic=profile_pic)
            profile.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserCreationForm()
    return render(request, 'core/registration.html',
                  {'user_form': user_form,
                   'registered': registered})


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            user_pref = UserProfileInfo.objects.get(user=user)
            return render(request, 'core/home.html', {'bio': user_pref.bio, 'pic': user_pref.profile_pic})
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
        return render(request, 'core/mytweets.html',{'tweets_all':tweets_all})
    else:
        tweets_all = u.tweets.all()
        return render(request, 'core/mytweets.html',{'tweets_all':tweets_all})




def search_profile(request):
    user_list = UserProfileInfo.objects.all()
    return render(request, 'core/search.html', {'user_list': user_list})


def get_profile(request, userid):
    followed = False
    user = UserProfileInfo.objects.get(user_id=userid)
    tweets = Tweet.objects.filter(user_id=userid)
    follow_count = FollowRelation.objects.filter(follow=User(user.user_id), user=request.user).count()
    if request.method == 'POST':
        if follow_count == 0:  # to follow, create a user in FollowRelation
            f = FollowRelation(follow=User(user.user_id), user=request.user)
            f.save()
        else:  #to unfollow, delete the user from FollowRelation
            FollowRelation.objects.filter(follow=User(user.user_id), user=request.user).delete()
    follow_count = FollowRelation.objects.filter(follow=User(user.user_id), user=request.user).count()
    return render(request, 'core/profile.html', {'profile_user': user, 'all_tweets': tweets, 'follow_count': follow_count, 'me': request.user})



def post_like(request, tweet_id):
    u = request.user
    t = Tweet.objects.get(id=tweet_id)
    try:
        new_t = TweetLike.objects.create(tweet=t, liked_by=u )
        new_t.save()
    except IntegrityError:
        return HttpResponse("already liked")
    all_likes = TweetLike.objects.filter(tweet=t)
    return render(request, 'core/tweets_liked_by.html', {'all_likes': all_likes, 'tweet':t})



def get_followers(request, userid):
    user_profile = UserProfileInfo.objects.get(user_id=userid)
    u = User.objects.get(username=user_profile.user.username)
    return render(request, 'core/follower.html', {'all_followers':u.followed.all(), 'profile_user':u})


def get_following(request,userid):
    user_profile = UserProfileInfo.objects.get(user_id=userid)
    u = User.objects.get(username=user_profile.user.username)
    return render(request, 'core/following.html', {'all_following':u.following.all(), 'profile_user':user_profile })


def timeline(request):
    total_tweets = Tweet.objects.filter(Q(user=request.user) | Q(user__in=request.user.following.values_list('follow', flat=True)))
    paginator = Paginator(total_tweets, 3)
    page = request.GET.get('page')
    my_tweets = paginator.get_page(page)
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

def search_tweet(request):
    if request.method == 'GET':
        lookup_word = request.GET.get('search_word', None)
        if lookup_word:
            tweets = Tweet.objects.filter(contents__icontains=lookup_word)
            return render(request, 'core/search_in_tweet.html', {'tweets': tweets})
        else:
            return render(request, 'core/search_in_tweet.html', {})

