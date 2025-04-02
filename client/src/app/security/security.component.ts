import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-security',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './security.component.html',
  styleUrls: ['./security.component.css']
})
export class SecurityComponent implements OnInit {
  currentPassword = '';
  newPassword = '';
  confirmPassword = '';
  message = '';
  logs: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadSecurityLogs();
  }

  changePassword() {
    if (this.newPassword !== this.confirmPassword) {
      this.message = 'Las contraseñas nuevas no coinciden.';
      return;
    }

    this.http.put('/api/auth/profile/password/', {
      current_password: this.currentPassword,
      new_password: this.newPassword
    }).subscribe({
      next: () => {
        this.message = 'Contraseña actualizada con éxito';
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
      },
      error: () => {
        this.message = 'Error al cambiar la contraseña';
      }
    });
  }

  loadSecurityLogs() {
    this.http.get('/api/auth/security/logs/').subscribe({
      next: (data: any) => this.logs = data,
      error: () => this.logs = []
    });
  }
}
