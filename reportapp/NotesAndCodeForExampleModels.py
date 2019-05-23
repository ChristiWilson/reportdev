from django.db import models
from django.shortcuts import render, get_object_or_404
from django import forms

# Following a YouTube Video for creating nested comments
# This is a recursive type of relationship that I may want to implement for report


# Create a models for which the nested comments will reply to
# In models.py
class Blog(models.Model):
    # Only adding certain fields from example
    title = models.CharField(max_length=100)  # Change max length from 200 to 100
    content = models.TextField()
    slug = models.SlugField(max_length=100, help_text="Using title field")
    page = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.title


class Comment(models.Model):
    # Only adding certain fields from example
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="reply")


# I am going to be doing the data entry in the admin interface, just adding
# these fields to follow along as I am not going to running the code right now
# but would like to add the code if I decide to use this in the future.

# in forms.py
# from .model import Blog, Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


# from .models import Comment, Blog
# for the View(s)
# in views.py
def blog_view(request):
    posts = Blog.objects.all()
    return render(request,"reportapp/home.html", {"posts": posts})


def blog_details(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    return render(request, "reportapp/home.html", {"blog": post})


def comment_view(request,):
    pass
