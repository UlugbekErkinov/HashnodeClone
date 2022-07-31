from django.db import models
from helpers.models import BaseModel

# Create your models here.

class Author(BaseModel):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to="avatar/")


    bio = models.TextField()
    work_place = models.CharField(max_length=128,null=True)
    linkedin_link = models.CharField(max_length=128)
    instagram_link = models.CharField(max_length=128)
    facebook_link = models.CharField(max_length=128)
    github_link = models.CharField(max_length=128)

    posts_count = models.IntegerField(default=0)
    is_top = models.BooleanField(default=False)


class AuthorFollower(models.Model):
    followers = models.ManyToManyField('self', symmetrical=False,
                                       blank=True)

    def count_followers(self):
        return self.followers.count()

    def count_following(self):
        return Author.objects.filter(followers=self).count()
