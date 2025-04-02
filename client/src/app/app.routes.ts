import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';

export const routes: Routes = [
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: '',
        loadComponent: () =>
          import('./pages/home/home.component').then((m) => m.HomeComponent)
      },
      {
        path: 'foro',
        loadComponent: () =>
          import('./pages/community/community.component').then((m) => m.CommunityComponent)
      },
      {
        path: 'grupos',
        loadComponent: () =>
          import('./pages/groups/groups.component').then((m) => m.GroupsComponent)
      },
      {
        path: 'trabajo',
        loadComponent: () =>
          import('./pages/jobs/jobs.component').then((m) => m.JobsComponent)
      },
      {
        path: 'reportes',
        loadComponent: () =>
          import('./pages/reports/reports.component').then((m) => m.ReportesComponent)
      },
      {
        path: 'perfil',
        loadComponent: () =>
          import('./pages/profile/profile.component').then((m) => m.ProfileComponent)
      }
    ]
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.component').then(m => m.RegisterComponent)
  },
  {
    path: '**',
    redirectTo: '',
  }
];
