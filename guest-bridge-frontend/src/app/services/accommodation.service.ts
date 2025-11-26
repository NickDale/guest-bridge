import { Injectable } from '@angular/core';
import { BehaviorSubject, filter, Observable, switchMap, map, throwError, catchError } from 'rxjs';
import { ConnectionStatus, ConnectionType, Property } from '../models/property-connection';
import { AccommodationCreationRequest, Accomodation, AccomodationDetail } from '../models/accommodation';
import { environment } from 'src/enviroments/environment';
import { HttpClient } from '@angular/common/http';
import { UserService } from './user.service';

@Injectable({
  providedIn: 'root'
})
export class AccommodationService {
  private apiUrl = environment.apiUrl;
  private selectedAccomodationSubject = new BehaviorSubject<AccomodationDetail | null>(null);
  selectedAccomodation$ = this.selectedAccomodationSubject.asObservable();

  properties: Property[] = []

  constructor(
    private http: HttpClient,
    private userService: UserService
  ) {
    this.init();
  }

  init(): void {
    this.properties = [
      {
        id: 1,
        type: ConnectionType.SZALLAS_HU,
        lastCheck: new Date(),
        status: ConnectionStatus.FAILED
      },
      {
        id: 2,
        type: ConnectionType.VENDEGEM,
        lastCheck: new Date(),
        status: ConnectionStatus.FAILED
      }
    ]
  }

  listAccommodations(): Observable<Accomodation[]> {
    return this.userService.selectedUser$.pipe(
      filter(user => !!user),
      switchMap(user =>
        this.http.get<Accomodation[]>(`${this.apiUrl}/users/${user!.id}/accommodations`)
      )
    );
  }

  getById(accommodationId: number): Observable<AccomodationDetail> {
    return this.userService.selectedUser$.pipe(
      filter(user => !!user),
      switchMap(user =>
        this.http.get<AccomodationDetail>(`${this.apiUrl}/users/${user!.id}/accommodations/${accommodationId}`)
      )
    );
  }

  setSelected(accomodation: AccomodationDetail) {
    this.selectedAccomodationSubject.next(accomodation);
  }

  findByIdAndType(id: number, connectionType: ConnectionType): Observable<Property | undefined> {
    const localProperty = this.properties.find(p => p.type === connectionType);
    return this.http.get<boolean>(`${this.apiUrl}/accommodations/${id}/${this.getEnumKey(connectionType)}/connection-check`)
      .pipe(
        map(
          isConnected => {
            const status = isConnected ? ConnectionStatus.SUCCESS : ConnectionStatus.FAILED;
            if (localProperty) {
              localProperty.status = status;
              localProperty.lastCheck = new Date();
              return localProperty;
            }

            const newProperty: Property = {
              id: id,
              type: ConnectionType.VENDEGEM,
              status: status,
              lastCheck: new Date(),
            };
            return newProperty;
          }
        )
      );
  }

  getEnumKey(value: ConnectionType): string | undefined {
    for (const key in ConnectionType) {
      if (ConnectionType[key as keyof typeof ConnectionType] === value) {
        return key;
      }
    }
    return undefined;
  }

  registerNewAccommodation(creationRequest: AccommodationCreationRequest) {
    return this.userService.selectedUser$.pipe(
      filter(user => !!user),
      switchMap(user => {
        creationRequest.user_id = user!.id
        return this.http.post<void>(`${this.apiUrl}/accommodations`, creationRequest).pipe(
          map(response => {
            return true;
          }),
          catchError(err => throwError(() => err))
        )
      }
      )
    );
  }

}

