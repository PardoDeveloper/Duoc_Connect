import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { tap } from 'rxjs/operators';
import { jwtDecode } from 'jwt-decode';
import { Observable } from 'rxjs';


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

  register(data: {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
  }) {
    return this.http.post('/api/auth/register/', data);
  }

  getUserEmail(): string {
    const token = localStorage.getItem('access');
    if (!token) return '';
    const decoded: any = jwtDecode(token);
    return decoded.email || '';
  }
  
  getUserProfile(): Observable<any> {
    return this.http.get(`/api/auth/profile/`);  // ✅ Correcto
  }
  

  updateProfilePhoto(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('profile_picture', file);  // <-- usa el nombre correcto aquí
    return this.http.put(`/api/auth/profile/photo/`, formData);
  }
  

  changePassword(currentPassword: string, newPassword: string): Observable<any> {
    return this.http.put(`/api/auth/profile/password/`, {
      current_password: currentPassword,
      new_password: newPassword
    });
  }

}
