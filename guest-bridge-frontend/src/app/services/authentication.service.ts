import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { Observable, map, catchError, of, BehaviorSubject } from "rxjs";
import { environment } from '../../enviroments/environment';


export interface LoggedUser {
  id: number;
  role: 'admin' | 'user';
  full_name: string
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = environment.apiUrl + '/authentications';
  private loggedInSubject = new BehaviorSubject<boolean>(this.isLoggedIn());
  public loggedIn$ = this.loggedInSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) { }

  login(username: string, password: string): Observable<boolean> {
    return this.http.post<LoggedUser>(`${this.apiUrl}/login`, { username: username, password: password }).pipe(
      map(response => {
        const user = {
          id: response.id,
          name: response.full_name,
          role: response.role
        };
        sessionStorage.setItem('user', JSON.stringify(user));
        this.loggedInSubject.next(true);
        return true;
      }),
      catchError(err => {
        console.error('Hibás belépés', err);
        return of(false);
      })
    );
  }

  getUser(): LoggedUser | null {
    const userJson = sessionStorage.getItem('user');
    if (userJson) {
      const user = JSON.parse(userJson);
      console.log(user.id, user.name, user.role);
      return user;
    }
    return null;
  }

  getUserName() {
    const user = sessionStorage.getItem('user');
    return user ? JSON.parse(user).name : undefined;
  }

  isLoggedIn(): boolean {
    return !!sessionStorage.getItem('user');
  }

  logout(): void {
    sessionStorage.clear();
    this.loggedInSubject.next(false);
  }
}