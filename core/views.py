from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.db.models import Q
from django.db import IntegrityError
from django.db import transaction

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render

from django.urls import reverse


# local imports
from .forms import  UserCreationForm, User
from .models import FollowRelation, Tweet, TweetLike,  UserProfileInfo


def index(request):
    return render(request, 'core/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@transaction.atomic()
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
    user = request.user
    if request.method == 'POST':
        new_tweet = request.POST.get('submit_tweet')
        Tweet.objects.create(contents=new_tweet, user=user)
        tweets_all = user.tweets.all()
        return render(request, 'core/mytweets.html',{'tweets_all':tweets_all})
    else:
        tweets_all = user.tweets.all()
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
        else:  # to unfollow, delete the user from FollowRelation
            FollowRelation.objects.filter(follow=User(user.user_id), user=request.user).delete()
    follow_count = FollowRelation.objects.filter(follow=User(user.user_id), user=request.user).count()
    return render(request, 'core/profile.html', {'profile_user': user, 'all_tweets': tweets,
                                                 'follow_count': follow_count, 'me': request.user})


def post_like(request, tweet_id):
    user = request.user
    tweet = Tweet.objects.get(id=tweet_id)
    try:
        new_tweet_like = TweetLike.objects.create(tweet=tweet, liked_by=user )
        new_tweet_like.save()
    except IntegrityError:
        return HttpResponse("already liked")
    all_likes = TweetLike.objects.filter(tweet=tweet)
    return render(request, 'core/tweets_liked_by.html', {'all_likes': all_likes, 'tweet': tweet})


def get_followers(request, userid):
    user_profile = UserProfileInfo.objects.get(user_id=userid)
    user = User.objects.get(username=user_profile.user.username)
    return render(request, 'core/follower.html', {'all_followers': user.followed.all(), 'profile_user': user})


def get_following(request,userid):
    user_profile = UserProfileInfo.objects.get(user_id=userid)
    user = User.objects.get(username=user_profile.user.username)
    return render(request, 'core/following.html', {'all_following': user.following.all(), 'profile_user': user_profile})


def timeline(request):
    total_tweets = Tweet.objects.filter(Q(user=request.user) |
                                        Q(user__in=request.user.following.values_list('follow', flat=True)))
    try:
        paginator = Paginator(total_tweets, 3, allow_empty_first_page=False)
        page = request.GET.get('page')
        my_tweets = paginator.get_page(page)
    except:
        return HttpResponse("No Tweet to show")
    return render(request, 'core/timeline.html', {'my_tweets': my_tweets})



def edit_bio(request):
    if request.method == 'POST':
        user = request.user
        updated_bio = request.POST.get('updated_bio')
        user_prof = UserProfileInfo.objects.get(user=user)
        user_prof.bio = updated_bio
        user_prof.save()
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

