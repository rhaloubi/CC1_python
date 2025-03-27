from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author_name = models.CharField(max_length=100, blank=True, help_text='Name for non-registered users')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Comment by {self.author.username if self.author else self.author_name} on {self.post.title}'
