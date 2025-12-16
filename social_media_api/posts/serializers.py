from rest_framework import serializers
from .models import Post, Comments

class PostSerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField(read_only=True)

  class Meta:
    model = Post
    fields = ['id','author','title', 'content', 'created_at', 'updated_at',]

class CommentSerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField(read_only=True)
  post = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Comments
    fields = ['author','id','post', 'content', 'created_at', 'updated_at']


