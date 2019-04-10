from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200,default="Add bio", null=True, blank=True)
    profile_pic = models.ImageField(upload_to='pictures', blank=True)

    def __str__(self):
        return str(self.user.username) + str(self.bio)


class TweetManager(models.Manager):
    def create_documents(self):
        vector = SearchVector('contents')
        return self.get_queryset().annotate(document=vector)


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    contents = models.CharField(max_length=120)
    published_time = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True)
    objects = TweetManager()

    def __str__(self):
        return str(self.contents) + str(self.published_time)

    class Meta:
        ordering = ('-published_time',)
        indexes = [
            GinIndex(fields=['search_vector'])
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if 'update_fields' not in kwargs or 'search_vector' not in kwargs['update_fields']:
            instance_doc = Tweet.objects.create_documents().get(pk=self.pk)
            instance_doc.search_vector = instance_doc.document
            instance_doc.save(update_fields=['search_vector'])

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

class TweetWord(models.Model):
    words = models.CharField(max_length=120, db_index=True)
    #tweet_id = models.ForeignKey(Tweet, on_delete=models.CASCADE)

