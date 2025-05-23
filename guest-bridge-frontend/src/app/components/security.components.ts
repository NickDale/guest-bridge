import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/authentication.service';


export function isAdmin(user: { role?: string } | null | undefined): boolean {
  return (user?.role ?? '').toLowerCase() === 'admin';
}

export const adminGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const user = auth.getUser();

  if (isAdmin(user)) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};

export const userDetailsGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  
  const userIdParam = +route.params['id'];
  const currentUser = auth.getUser();

  if (!currentUser) {
    router.navigate(['/login']);
    return false;
  }

  if (isAdmin(currentUser)) {
    return true;
  }

  if (currentUser.id === userIdParam) {
    return true;
  } else {
    router.navigate([`/users/${currentUser.id}`]);
    return false;
  }

  return false;
};