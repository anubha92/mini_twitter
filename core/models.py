from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200,default="Add bio", null=True, blank=True)
    profile_pic = models.ImageField(upload_to='pictures', blank=True)

    def __str__(self):
        return str(self.user.username) + str(self.bio)


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    contents = models.CharField(max_length=120)
    published_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.contents) + str(self.published_time)

    class Meta:
        ordering = ('-published_time',)


class FollowRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    def __str__(self):
        return str(self.user) + str(self.follow)


class TweetLike(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.liked_by.username)

    class Meta:
        unique_together = ("tweet", "liked_by")