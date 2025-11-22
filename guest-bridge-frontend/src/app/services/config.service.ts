import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, filter, switchMap, map } from 'rxjs';
import { environment } from 'src/enviroments/environment';
import { AccomodationDetail, Accomodation } from '../models/accommodation';
import { Property, ConnectionType, ConnectionStatus } from '../models/property-connection';
import { UserService } from './user.service';
import { MapRecord, Room, RoomMapping } from '../models/room';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  private apiUrl = environment.apiUrl;
  //private selectedAccomodationSubject = new BehaviorSubject<AccomodationDetail | null>(null);
  //selectedAccomodation$ = this.selectedAccomodationSubject.asObservable();



  properties: Property[] = []

  constructor(private http: HttpClient) {
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

  listAccommoddationMappingConfiguration(id: number): Observable<{ szallasHuRooms: Room[], vendegemRooms: Room[], mapping: RoomMapping }> {
    const url = `${this.apiUrl}/accommodations/${id}/mapping-configuration`;

    return this.http.get<MapRecord[]>(url).pipe(
      map(records => {

        const szallasHuRooms: Room[] = [];
        const vendegemRoomsMap: Room[] = [];
        const mapping: RoomMapping = {};

        records.forEach(record => this.mapper(record, szallasHuRooms, vendegemRoomsMap, mapping)
        );
        return {
          szallasHuRooms: szallasHuRooms,
          vendegemRooms: vendegemRoomsMap,
          mapping: mapping,
        };
      })
    );
  }

  private mapper(record: MapRecord, szallasHuRooms: Room[], vendegemRoomsMap: Room[], mapping: RoomMapping) {
    {
      const szhRoom: Room = {
        id: record.id,
        externalId: record.szallas_hu_ext_room_id,
        name: record.szallas_hu_ext_room_name,
      };

      szallasHuRooms.push(szhRoom);
      const vgRoom: Room = {
        id: record.id,
        externalId: record.vendegem_ext_room_id,
        name: record.vendegem_ext_room_name,
      };

      vendegemRoomsMap.push(vgRoom);
      mapping[String(szhRoom.id)] = String(vgRoom.id);
    }
  }

  getEnumKey(value: ConnectionType): string | undefined {
    for (const key in ConnectionType) {
      if (ConnectionType[key as keyof typeof ConnectionType] === value) {
        return key;
      }
    }
    return undefined;
  }
}
