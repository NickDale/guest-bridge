import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { Observable, map, catchError, of } from "rxjs";
import { environment } from '../../enviroments/environment';


export interface LoginResponse {
  id: number;
  role: 'admin' | 'user';
  // akár token is, ha van: token: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = environment.apiUrl + '/authentications';

  constructor(private http: HttpClient, private router: Router) { }
  login(username: string, password: string): Observable<boolean> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, { username: username, password: password }).pipe(
      map(response => {
        sessionStorage.setItem('userId', response.id.toString());
        sessionStorage.setItem('role', response.role);

        console.log('RESPONSEEEE')
        console.log(response)
        return true;
      }),
      catchError(err => {
        console.error('Hibás belépés', err);
        return of(false);
      })
    );
  }

  logout() {
    sessionStorage.clear();
    this.router.navigate(['/login']);
  }

  getUser(): { id: number, role: 'user' | 'admin' } | null {
    const id = +sessionStorage.getItem('userId')!;
    const role = sessionStorage.getItem('role') as 'user' | 'admin' | null;

    if (id && role) {
      return { id, role };
    }
    return null;
  }

  isLoggedIn(): boolean {
    return this.getUser() !== null;
  }

  hasPermission(targetUserId: number): boolean {
    const user = this.getUser();
    if (!user) {
      return false;
    }
    if (user.role === 'admin') {
      return true;
    }
    return user.id === targetUserId;
  }
}