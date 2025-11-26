import { Injectable } from '@angular/core';
import { UpdateUserRequest, User } from '../models/user';
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

  updateUser(user_id: number, updateRequest: UpdateUserRequest): Observable<boolean> {
    return this.http.patch<void>(`${this.apiUrl}/users/${user_id}`, updateRequest).pipe(
      map(response => {
        console.log(`Sikeres user [${user_id}] update  rögzites sikres`);
        return true;
      }),
      catchError(err => {
        console.log(`Error a user [${user_id}] update  során`);
        return throwError(() => err);
      })
    );
  }

  changePassword(userId: number, oldPassword: string, newPassword: string): Observable<boolean> {
    return this.http.patch<void>(`${this.apiUrl}/users/${userId}/change-password`, { old_password: oldPassword, new_password: newPassword }).pipe(
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

  registerUser(name: string, email: string): Observable<boolean> {
    return this.http.patch<void>(`${this.apiUrl}/users`, { name: name, email: email }).pipe(
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

  deactivate(userId: number): Observable<boolean> {
    return this.http.delete<void>(`${this.apiUrl}/users/${userId}/inactivate`).pipe(
      map(response => {
        console.log('Sikeres inaktiválás', response);
        return true;
      }),
      catchError(err => {
        console.error('Hiba az inaktiválásban:', err);
        return throwError(() => err);
      })
    );
  }

  activate(userId: number): Observable<boolean> {
    return this.http.patch<void>(`${this.apiUrl}/users/${userId}/activate`, {}).pipe(
      map(response => {
        console.log('Sikeres aktiválás', response);
        return true;
      }),
      catchError(err => {
        console.error('Hiba az aktiválásban:', err);
        return throwError(() => err);
      })
    );
  }
}
