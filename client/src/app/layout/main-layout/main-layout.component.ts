import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-main-layout',
  imports: [CommonModule, RouterOutlet],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.css'
})
export class MainLayoutComponent {
  userEmail: string | null = null;
  currentSection = 'Home';

  constructor(private auth: AuthService, private router: Router) {
    const user = this.auth.getCurrentUser();
    this.userEmail = user?.email || 'Estudiante';

    // Detecta cambios de ruta y asigna el título
    this.router.events.subscribe(() => {
      const route = this.router.url;
      if (route.includes('/foro')) this.currentSection = 'Comunidad';
      else if (route.includes('/grupos')) this.currentSection = 'Grupos de Estudio';
      else if (route.includes('/trabajo')) this.currentSection = 'Bolsa de Trabajo';
      else if (route.includes('/denuncias')) this.currentSection = 'Seguridad';
      else if (route.includes('/perfil')) this.currentSection = 'Mi Perfil';
      else this.currentSection = 'Home';
    });
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }

}
