import { Injectable } from '@angular/core';
import { BehaviorSubject, filter, Observable, switchMap, map, throwError, catchError, interval, delay, takeWhile, tap } from 'rxjs';
import { ConnectionStatus, ConnectionType, Property } from '../models/property-connection';
import { AccommodationCreationRequest, Accomodation, AccomodationDetail } from '../models/accommodation';
import { environment } from 'src/enviroments/environment';
import { HttpClient } from '@angular/common/http';
import { UserService } from './user.service';
import { ExternalLoginResponse, SessionStatusResponse } from '../models/external-connection';

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


  getSessionStatus(accommodationId: number, connectionType: ConnectionType, sessionId: string): Observable<SessionStatusResponse> {
    return this.http.get<SessionStatusResponse>(
      `${this.apiUrl}/accommodations/${accommodationId}/${this.getEnumKey(connectionType)}/session-status-check/${sessionId}`,
    );
  }

  submit2faCode(accommodationId: number, connectionType: ConnectionType, sessionId: string, code: string): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/accommodations/${accommodationId}/${this.getEnumKey(connectionType)}/verify`,
      { session_id: sessionId, code: code }
    );
  }

  externalLogin(accommodationId: number, connectionType: ConnectionType, username: string, password: string): Observable<SessionStatusResponse> {
    return this.http.post<ExternalLoginResponse>(
      `${this.apiUrl}/accommodations/${accommodationId}/${this.getEnumKey(connectionType)}/login`,
      { username: username, password: password }
    )
    .pipe(
        delay(2000), 
        
        switchMap(res => {
            const sessionId = res.session_id;

            return this.getSessionStatus(accommodationId, connectionType, sessionId); 
        })
    );
     /* .pipe(
        switchMap(
          res => {
            const sessionId = res.session_id

            return interval(2000).pipe(
                // Várjunk egy keveset az első lekérdezés előtt, hogy a backend is elinduljon
                delay(100), 
                switchMap(() => this.getSessionStatus(accommodationId,connectionType,sessionId)), 
                
                // takeWhile: Addig megy a polling, amíg nincs DONE vagy WAITING_2FA vagy FAILED
                takeWhile(status => status.step !== 'done' && status.step !== 'waiting_2fa' && status.step !== 'failed', true),
                
                // Visszaadja az utolsó állapotot (ami az exit condition volt)
                tap(status => {
                    // Itt megállítjuk a pollingot, de az utolsó értéket átadjuk a feliratkozónak
                    if (status.step === 'done' || status.step === 'failed' || status.step === 'waiting_2fa') {
                        // A takeWhile leállítja a streamet
                    }
                }),
                
                // Ez a map csak az utolsó értéket adja át
                map(status => status) 
            );
          }
        )
      );*/
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

