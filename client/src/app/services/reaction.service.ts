import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ReactionService {
  private baseUrl = '/api/community/posts/';

  constructor(private http: HttpClient) {}

  react(postId: number, reaction_type: string): Observable<any> {
    return this.http.post(`${this.baseUrl}${postId}/react/`, { reaction_type });
  }
}
