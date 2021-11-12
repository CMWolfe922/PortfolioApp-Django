from django.db import models

# Create your models here.
# First I need to create a catgory class for my blog posts


class Category(models.Model):
    name = models.CharField(max_length=20)

# Now create the Post class and create a relatioship between posts
# and categories. A ManyToManyField


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')

# Last model to create is the comment model. This will allow users to
# comment on the Posts. I will create a ManyToOne relationship between
# posts and comments using ForeignKeyField


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # Now create the relationship to a single post
    # many comments to one post
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
