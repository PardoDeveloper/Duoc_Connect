from rest_framework import serializers
from .models import Post, Comment, Reaction

class PostSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_email', 'created_at', 'updated_at', 'is_public']


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author_email', 'created_at']


class ReactionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'post', 'reaction_type', 'user_email', 'created_at']
