import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PostServiceService {
  private apiUrl = '/api/community/posts/';

  constructor(private http: HttpClient) {}

  getPosts() {
    return this.http.get<any[]>(this.apiUrl);
  }

  createPost(data: { title: string; content: string; is_public: boolean }) {
    return this.http.post(this.apiUrl, data);
  }
}
