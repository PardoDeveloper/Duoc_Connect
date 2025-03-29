from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)  # Para futuras publicaciones privadas

    def __str__(self):
        return f"{self.title} - {self.author.email}"

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.email} → {self.post.title[:30]}"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍 Me gusta'),
        ('love', '❤️ Me encanta'),
        ('laugh', '😂 Me divierte'),
        ('sad', '😢 Me entristece'),
        ('angry', '😡 Me enoja'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Evita múltiples reacciones de un mismo usuario al mismo post

    def __str__(self):
        return f"{self.user.email} reaccionó con {self.reaction_type} a {self.post.title}"
