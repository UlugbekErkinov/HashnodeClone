from django.db import models
from common.models import User
from helpers.models import BaseModel
from feed.models import Post
# Create your models here.

class Bookmark(BaseModel):
    user = models.ForeignKey(User,on_delete = models.CASCADE, related_name='user_bookmark')
    story = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='story_bookmark')



