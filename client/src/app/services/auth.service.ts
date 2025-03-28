import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { tap } from 'rxjs/operators';
import { jwtDecode } from 'jwt-decode';


export interface JwtPayload {
  email: string;
  exp: number;
  // Agrega más campos si tu JWT los tiene (como nombre, rol, etc.)
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = '/api/auth/login/';

  constructor(private http: HttpClient) {}

  login(email: string, password: string) {
    return this.http.post<any>(this.apiUrl, { email, password }).pipe(
      tap(res => {
        localStorage.setItem('access', res.access);
        localStorage.setItem('refresh', res.refresh);
      })
    );
  }

  logout() {
    localStorage.clear();
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('access');
    if (!token) return false;

    try {
      const decoded: JwtPayload = jwtDecode(token);
      const now = Date.now() / 1000;
      return decoded.exp > now;
    } catch (err) {
      return false;
    }
  }

  getCurrentUser(): JwtPayload | null {
    const token = localStorage.getItem('access');
    if (!token) return null;
  
    try {
      return jwtDecode<JwtPayload>(token);
    } catch (error) {
      return null;
    }
  }
}
