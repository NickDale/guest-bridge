import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, map, catchError, BehaviorSubject, throwError } from "rxjs";
import { environment } from '../../enviroments/environment';
import { AuthResponse, LoggedUser } from "../models/authentication";


@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = environment.apiUrl + '/authentications';
  private loggedInSubject = new BehaviorSubject<boolean>(this.isLoggedIn());
  public loggedIn$ = this.loggedInSubject.asObservable();

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<boolean> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, { username: username, password: password }).pipe(
      map(response => {
        const user = {
          id: response.user.id,
          name: response.user.full_name,
          role: response.user.role
        };
        sessionStorage.setItem('user', JSON.stringify(user));
        sessionStorage.setItem('token', response.access_token);
        this.loggedInSubject.next(true);
        return true;
      }),
      catchError(err => {
        console.error('Hibás belépés', err);
        return throwError(() => err);
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

  getToken() {
    return sessionStorage.getItem('token')
  }

  logout(): void {
    sessionStorage.clear();
    this.loggedInSubject.next(false);
  }
}