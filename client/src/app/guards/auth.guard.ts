import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {

  const router = inject(Router);
  const token = localStorage.getItem('access');

  if (!token) {
    router.navigate(['/login']);
    return false;
  }

  return true;
};
