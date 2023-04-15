from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    followers = models.ManyToManyField(User, related_name="get_followers")
    following = models.ManyToManyField(User, related_name="get_following")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)


    def serialize(self, user):
        return{
            "username": self.user.username,
            "followers" : self.followers,
            "following" :self.following, 
        }

    def __str__(self):
        return self.slug

class Post(models.Model):
    body = models.CharField(max_length =200)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="author")
    created_on = models.DateTimeField(auto_now_add =True)
    liked = models.ManyToManyField(Profile, null=True, blank=True, related_name="likes")

    def __str__(self):
        return self.body.split(" ")[0]

    def serialize(self):
        return{
            "id": self.id,
            "user": self.author,
            "body": self.body,
            "created_on": self.created_on,
            "likes": self.liked.count(),
            
        }


class Comment(models.Model):
    pass


# class Likes(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, )
#     user = models.ForeignKey(User, )