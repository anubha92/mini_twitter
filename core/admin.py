from django.contrib import admin
from .models import UserProfileInfo,Tweet, FollowRelation
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Tweet)
admin.site.register(FollowRelation)


