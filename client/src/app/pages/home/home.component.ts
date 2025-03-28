import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  userEmail: string | null = null;

  constructor(private auth: AuthService, private router: Router) {
    const user = this.auth.getCurrentUser();
    this.userEmail = user?.email || null;
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
