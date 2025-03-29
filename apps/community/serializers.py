from rest_framework import serializers
from .models import Post, Comment, Reaction
from django.db import models


# Diccionario de emojis para usar en todos lados
Reaction.REACTION_CHOICES_DICT = dict(Reaction.REACTION_CHOICES)


class ReactionCountSerializer(serializers.Serializer):
    emoji = serializers.CharField()
    count = serializers.IntegerField()


class PostSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)
    reaction_counts = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_email', 'title', 'content', 'created_at', 'reaction_counts', 'user_reaction']

    def get_reaction_counts(self, obj):
        counts = (
            obj.reactions
            .values('reaction_type')
            .annotate(count=models.Count('id'))
            .order_by('-count')
        )
        return [
            {
                'emoji': Reaction.REACTION_CHOICES_DICT.get(rc['reaction_type'], rc['reaction_type']),
                'count': rc['count']
            }
            for rc in counts
        ]

    def get_user_reaction(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            reaction = obj.reactions.filter(user=user).first()
            if reaction:
                return Reaction.REACTION_CHOICES_DICT.get(reaction.reaction_type)
        return None


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_email', 'content', 'created_at']
        read_only_fields = ['author_email', 'created_at', 'post']


class ReactionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'post', 'user_email', 'reaction_type', 'created_at']
        read_only_fields = ['user_email', 'created_at', 'post']
