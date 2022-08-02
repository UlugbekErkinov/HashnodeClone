from django.db import models
from helpers.models import BaseModel
from author.models import Author
from common.models import User
from model_utils import Choices
from django.utils.translation import gettext as _


# Create your models here.


class Tag(BaseModel):
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)


class Post(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Nomi')
    slug = models.CharField(max_length=128, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to="post/", null=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='posts')
    website_url = models.URLField()

    tags = models.ManyToManyField(Tag, related_name='posts')

    published_date = models.DateField(null=True)
    read_min = models.IntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    personalized = models.BooleanField(default=False)
    STATUS = Choices(('draft', _('draft')), ('published', _('published')))
    saved = models.ManyToManyField(User, related_name="saveds", blank=True)


class Comment(BaseModel):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name="blog_comment", blank=True)
    emoji = models.CharField(max_length=128, default = None, null =True,  unique=True)
    reply = models.ForeignKey(
        'self', null=True, related_name="replies", on_delete=models.CASCADE)

    def total_clicks(self):
        return self.likes.count()

    def __str__(self):
        return '%s - %s - %s' % (self.post.title, self.name, self.id)


class Bookmark(BaseModel):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author_bookmark')
    story = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='story_bookmark')
