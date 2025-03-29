import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { PostServiceService } from '../../services/post-service.service';

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

  constructor(private postService: PostServiceService) {}

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
}
