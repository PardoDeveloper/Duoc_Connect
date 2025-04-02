import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  user: any = {};
  defaultAvatar = 'assets/avatar-placeholder.png';
  selectedFile: File | null = null;
  previewUrl: string | null = null;

  currentPassword = '';
  newPassword = '';
  confirmPassword = '';
  message = '';
  passwordMismatch = false;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.authService.getUserProfile().subscribe({
      next: (data) => {
        this.user = data;
        this.previewUrl = data.profile_picture || null;
      },
      error: () => console.error('Error al cargar perfil')
    });
  }

  onPhotoSelected(event: any) {
    const input = event.target;
    const file = input.files[0];
    if (file) {
      this.selectedFile = file;

      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.previewUrl = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    input.value = ''; // permite volver a seleccionar la misma imagen
  }

  uploadPhoto() {
    if (!this.selectedFile) {
      alert('Por favor selecciona una imagen primero');
      return;
    }

    this.authService.updateProfilePhoto(this.selectedFile).subscribe({
      next: () => {
        this.message = 'Foto actualizada correctamente';
        this.selectedFile = null;
        this.previewUrl = null;
        this.loadProfile();
      },
      error: () => this.message = 'Error al subir la foto'
    });
  }

  changePassword() {
    this.message = '';
    this.passwordMismatch = false;

    if (!this.currentPassword || !this.newPassword || !this.confirmPassword) {
      this.message = 'Debes completar todos los campos.';
      return;
    }

    if (this.newPassword !== this.confirmPassword) {
      this.passwordMismatch = true;
      return;
    }

    this.authService.changePassword(this.currentPassword, this.newPassword).subscribe({
      next: () => {
        this.message = 'Contraseña actualizada con éxito';
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
        this.passwordMismatch = false;
      },
      error: (err) => {
        this.message = err.error?.error || 'Error al cambiar contraseña';
      }
    });
  }
}
  