import { Injectable, OnInit } from '@angular/core';
import { User } from '../models/user';
import { BehaviorSubject, catchError, map, Observable, of, throwError } from 'rxjs';
import { environment } from 'src/enviroments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = environment.apiUrl;
  private selectedUserSubject = new BehaviorSubject<User | null>(null);
  selectedUser$ = this.selectedUserSubject.asObservable();

  users: User[] = []

  constructor(private http: HttpClient) {
  }

  mockedData() {
    return this.users;
  }

  listUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users?expect=admin`)
  }

  getUserById(userId: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/` + userId)
  }

  setSelectedUser(user: User) {
    this.selectedUserSubject.next(user);
  }

  registerUser(name: string, email: string): Observable<boolean> {
    return this.http.post<void>(`${this.apiUrl}/users`, { name: name, email: email }).pipe(
      map(response => {
        console.log('User rögzites sikres', response);
        return true;
      }),
      catchError(err => {
        console.error('Hibás regisztráció a service-ben:', err);
        return throwError(() => err);
      })
    );
  }
}
