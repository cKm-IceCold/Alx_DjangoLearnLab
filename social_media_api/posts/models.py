from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
  
  def __str__(self):
    return self.title

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

  author = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_comments')

  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Comment by {self.author}"

