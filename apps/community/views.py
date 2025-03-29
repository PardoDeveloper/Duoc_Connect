from rest_framework import generics, permissions, status
from .models import Post, Comment, Reaction
from .serializers import PostSerializer, CommentSerializer, ReactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(is_public=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise permissions.PermissionDenied("Solo puedes editar tus propias publicaciones.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("Solo puedes eliminar tus propias publicaciones.")
        instance.delete()

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # 👈 Esto desactiva la paginación SOLO para comentarios

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id']).order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)  # <- ¡AQUÍ importante!

class ReactionCreateUpdateView(generics.CreateAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        reaction_type = request.data.get('reaction_type')

        if reaction_type not in dict(Reaction.REACTION_CHOICES):
            return Response({'error': 'Tipo de reacción no válido'}, status=status.HTTP_400_BAD_REQUEST)

        reaction, _ = Reaction.objects.update_or_create(
            post_id=post_id,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )

        serializer = self.get_serializer(reaction)
        return Response(serializer.data)