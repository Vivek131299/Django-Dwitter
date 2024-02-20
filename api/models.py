from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    # Profile for the user will be created automatically (using signal in signals.py) when a new user is created.

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()


class Dweet(models.Model):
    user = models.ForeignKey(User, related_name='dweets', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:20]}..."
        )


class Like(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile_likes', on_delete=models.DO_NOTHING)
    dweet = models.ForeignKey(Dweet, related_name='dweet_likes', on_delete=models.CASCADE)

    @property
    def likes_count(self):
        return Like.objects.filter(dweet=self.dweet).count()


class Comment(models.Model):
    profile = models.ForeignKey(Profile, related_name="profile_comments", on_delete=models.DO_NOTHING)
    dweet = models.ForeignKey(Dweet, related_name="dweet_comments", on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def comments_count(self):
        return Comment.objects.filter(dweet=self.dweet).count()


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

