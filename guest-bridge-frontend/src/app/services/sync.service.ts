import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { SyncRecord } from '../models/sync';
import { environment } from 'src/enviroments/environment';

@Injectable({
  providedIn: 'root'
})
export class SyncService {

  private apiUrl = environment.apiUrl;
  constructor(private http: HttpClient) { }

  getSyncHistory(id: number): Observable<SyncRecord[]> {
    // A hívás, ami visszaadja a SyncRecord[] tömböt
    const url = `${this.apiUrl}/accommodations/${id}/sync-history`;
    return this.http.get<SyncRecord[]>(url);
  }
}
