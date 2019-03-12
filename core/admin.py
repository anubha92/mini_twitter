from django.contrib import admin
from .models import Tweet, FollowRelation, User, UserProfileInfo, TweetLike
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Tweet)
admin.site.register(FollowRelation)
admin.site.register(TweetLike)