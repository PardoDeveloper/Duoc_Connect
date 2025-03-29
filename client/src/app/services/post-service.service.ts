import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PostServiceService {
  private apiUrl = '/api/community/posts/';

  constructor(private http: HttpClient) {}

  getPosts(url: string = '') {
    const endpoint = url || this.apiUrl;
    return this.http.get<any>(endpoint);
  }

  createPost(data: { title: string; content: string; is_public: boolean }) {
    return this.http.post(this.apiUrl, data);
  }

  deletePost(postId: number) {
    return this.http.delete(`/api/community/posts/${postId}/`);
  }
}
