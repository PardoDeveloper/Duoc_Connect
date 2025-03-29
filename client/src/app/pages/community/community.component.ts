import { Component, OnInit } from '@angular/core';

import { FormsModule } from '@angular/forms';
import { PostServiceService } from '../../services/post-service.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-community',
  imports: [FormsModule, CommonModule],
  templateUrl: './community.component.html',
  styleUrl: './community.component.css'
})
export class CommunityComponent implements OnInit {

  posts: any[] = [];
  newPost = { title: '', content: '' };
  error = '';
  constructor(private postService: PostServiceService){}
  
  ngOnInit(): void {
    this.loadPosts();
  }

  loadPosts() {
    this.postService.getPosts().subscribe({
      next: (res) => (this.posts = res),
      error: () => (this.error = 'Error al cargar publicaciones.')
    });
  }

  createPost() {
    if (!this.newPost.title.trim() || !this.newPost.content.trim()) return;

    const postData = {
      ...this.newPost,
      is_public: true
    };

    this.postService.createPost(postData).subscribe({
      next: () => {
        this.newPost = { title: '', content: '' };
        this.loadPosts(); // Refresca la lista
      },
      error: () => (this.error = 'No se pudo publicar.')
    });
  }
}
