import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { PostServiceService } from '../../services/post-service.service';
import { CommentService } from '../../services/comment.service';
import { ReactionService } from '../../services/reaction.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-community',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './community.component.html',
  styleUrls: ['./community.component.css']
})
export class CommunityComponent implements OnInit, OnDestroy {
  posts: {
    id: number;
    author_email: string;
    title: string;
    content: string;
    created_at: string;
    reaction_counts: { emoji: string; count: number }[];
    user_reaction?: string;
  }[] = [];

  newPost = { title: '', content: '' };
  nextPage: string | null = null;
  previousPage: string | null = null;
  error = '';
  pollingInterval: any;

  commentsMap: { [postId: number]: any[] } = {};
  newCommentsMap: { [postId: number]: string } = {};
  showCommentsMap: { [postId: number]: boolean } = {};

  userEmail: string = '';
  showDeleteModal: number | null = null;

  constructor(
    private postService: PostServiceService,
    private commentService: CommentService,
    private reactionService: ReactionService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.userEmail = this.authService.getUserEmail();
    this.loadPosts();
    this.pollingInterval = setInterval(() => this.loadPosts(), 15000);
  }

  ngOnDestroy(): void {
    clearInterval(this.pollingInterval);
  }

  loadPosts(url: string = ''): void {
    this.postService.getPosts(url).subscribe({
      next: (res) => {
        this.posts = res.results ?? res;
        this.nextPage = res.next || null;
        this.previousPage = res.previous || null;
      },
      error: () => {
        this.error = 'Error al cargar publicaciones.';
      }
    });
  }

  next(): void {
    if (this.nextPage) this.loadPosts(this.nextPage);
  }

  previous(): void {
    if (this.previousPage) this.loadPosts(this.previousPage);
  }

  createPost(): void {
    if (!this.newPost.title.trim() || !this.newPost.content.trim()) return;

    const postData = {
      ...this.newPost,
      is_public: true
    };

    this.postService.createPost(postData).subscribe({
      next: () => {
        this.newPost = { title: '', content: '' };
        this.loadPosts();
      },
      error: () => {
        this.error = 'No se pudo publicar.';
      }
    });
  }

  toggleComments(postId: number): void {
    this.showCommentsMap[postId] = !this.showCommentsMap[postId];
    if (this.showCommentsMap[postId] && !this.commentsMap[postId]) {
      this.loadComments(postId);
    }
  }

  loadComments(postId: number): void {
    this.commentService.getComments(postId).subscribe({
      next: (comments) => {
        this.commentsMap[postId] = comments.results ?? comments;
      },
      error: () => {
        this.commentsMap[postId] = [];
      }
    });
  }

  addComment(postId: number): void {
    const content = this.newCommentsMap[postId];
    if (!content?.trim()) return;

    this.commentService.addComment(postId, content).subscribe({
      next: () => {
        this.newCommentsMap[postId] = '';
        this.showCommentsMap[postId] = true;
        this.loadComments(postId);
      },
      error: () => alert('No se pudo agregar el comentario.')
    });
  }

  reactToPost(postId: number, type: string): void {
    this.reactionService.react(postId, type).subscribe({
      next: () => this.loadPosts(),
      error: () => alert('No se pudo registrar la reacción.')
    });
  }

  // 🔥 Modal: abre confirmación
  openDeleteModal(postId: number): void {
    this.showDeleteModal = postId;
  }

  cancelDelete(): void {
    this.showDeleteModal = null;
  }

  confirmDeletePost(): void {
    if (!this.showDeleteModal) return;

    this.postService.deletePost(this.showDeleteModal).subscribe({
      next: () => {
        this.posts = this.posts.filter(p => p.id !== this.showDeleteModal);
        this.cancelDelete();
      },
      error: () => {
        this.error = 'Error al eliminar publicación';
        this.cancelDelete();
      }
    });
  }
}
