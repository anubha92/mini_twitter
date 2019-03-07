from django.contrib import admin
from .models import UserProfileInfo,Tweets, Followers
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Tweets)
admin.site.register(Followers)


