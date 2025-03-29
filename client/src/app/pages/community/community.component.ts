import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { PostServiceService } from '../../services/post-service.service';
import { CommentService } from '../../services/comment.service';

@Component({
  selector: 'app-community',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './community.component.html',
  styleUrls: ['./community.component.css']
})
export class CommunityComponent implements OnInit, OnDestroy {
  posts: any[] = [];
  newPost = { title: '', content: '' };
  nextPage: string | null = null;
  previousPage: string | null = null;
  error = '';
  pollingInterval: any;

  // 👇 Estas tres son para manejar los comentarios por publicación
  commentsMap: { [postId: number]: any[] } = {};
  newCommentsMap: { [postId: number]: string } = {};
  showCommentsMap: { [postId: number]: boolean } = {};

  constructor(
    private postService: PostServiceService,
    private commentService: CommentService
  ) {}

  ngOnInit(): void {
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
    if (this.nextPage) {
      this.loadPosts(this.nextPage);
    }
  }

  previous(): void {
    if (this.previousPage) {
      this.loadPosts(this.previousPage);
    }
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
        this.loadPosts(); // refresca después de publicar
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
        console.log('Comentarios para post ' + postId, comments); // 👀 debug
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
        this.showCommentsMap[postId] = true; // 👈 abre comentarios si estaban ocultos
        this.loadComments(postId);
      },
      error: () => alert('No se pudo agregar el comentario.')
    });
  }
  
  
}
