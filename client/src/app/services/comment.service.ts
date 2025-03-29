import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CommentService {
  private baseUrl = '/api/community/posts/';

  constructor(private http: HttpClient) {}

  // ✅ Permite que Angular maneje tanto arrays simples como respuestas paginadas
  getComments(postId: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}${postId}/comments/`);
  }

  addComment(postId: number, content: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}${postId}/comments/`, { content });
  }
}
  