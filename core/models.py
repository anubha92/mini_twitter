from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200,default="Add bio")
   # profile_pic = models.ImageField(upload_to='profile_pics', null=True)

    def __str__(self):
        return (str(self.user.username) + str(self.bio))

class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True, related_name='tweets')
    contents = models.CharField(max_length=120)
    published_time = models.DateTimeField(auto_created=True, default=datetime.today())


    def __str__(self):
        return (str(self.contents) + str(self.published_time)) #, self.user_name

class Followers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name='followers')

    def __str__(self):
        return str(self.user.username)