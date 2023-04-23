from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="get_profile")
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
    
    def get_profile_following_posts(self):
        return self.following.all()

class Post(models.Model):
    body = models.CharField(max_length =200)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="posts")
    created_on = models.DateTimeField(auto_now_add =True)
    liked = models.ManyToManyField(Profile, null=True, blank=True, related_name="likes")

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

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
    
    # def get_profile_following_posts(self):
    #     return self.author.posts.order_by("_date").all()


class Comment(models.Model):
    pass

# class Following(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_following")
#     user_followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_followers")

#     def __str__(self):
#         return f"{self.user} is following {self.user_followed}"
    
#     def get_user_followed_posts(self):
#         return self.user_followed.posts.order_by("-date").all()


# class Likes(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, )
#     user = models.ForeignKey(User, )