from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, CommentListCreateView, ReactionCreateUpdateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),

    # Comentarios de un post
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),

    path('posts/<int:post_id>/react/', ReactionCreateUpdateView.as_view(), name='post-react'),
    
]
