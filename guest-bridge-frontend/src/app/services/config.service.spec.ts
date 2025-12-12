import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ConfigService } from './config.service';
import { environment } from 'src/enviroments/environment';
import { ConnectionType, ConnectionStatus } from '../models/property-connection';
import { MapRecord } from '../models/room';

describe('ConfigService', () => {
  let service: ConfigService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ConfigService]
    });
    service = TestBed.inject(ConfigService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('init', () => {
    it('should initialize properties with 2 items', () => {
      expect(service.properties.length).toBe(2);
    });

    it('should initialize properties with correct types', () => {
      expect(service.properties[0].type).toBe(ConnectionType.SZALLAS_HU);
      expect(service.properties[1].type).toBe(ConnectionType.VENDEGEM);
    });

    it('should initialize properties with FAILED status', () => {
      expect(service.properties[0].status).toBe(ConnectionStatus.FAILED);
      expect(service.properties[1].status).toBe(ConnectionStatus.FAILED);
    });

    it('should initialize properties with valid dates', () => {
      expect(service.properties[0].lastCheck).toBeInstanceOf(Date);
      expect(service.properties[1].lastCheck).toBeInstanceOf(Date);
    });
  });

  describe('listAccommoddationMappingConfiguration', () => {
    it('should call the correct endpoint', () => {
      const accommodationId = 123;
      const mockResponse: MapRecord[] = [];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe();

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });

    it('should map records correctly with full mapping', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [
        {
          id: 1,
          szallas_hu_ext_room_id: 'szh-101',
          szallas_hu_ext_room_name: 'Szállás.hu Room 1',
          vendegem_ext_room_id: 'vg-201',
          vendegem_ext_room_name: 'Vendégem Room 1',
          created_date: new Date()
        },
        {
          id: 2,
          szallas_hu_ext_room_id: 'szh-102',
          szallas_hu_ext_room_name: 'Szállás.hu Room 2',
          vendegem_ext_room_id: 'vg-202',
          vendegem_ext_room_name: 'Vendégem Room 2',
          created_date: new Date()
        }
      ];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        expect(result.szallasHuRooms.length).toBe(2);
        expect(result.vendegemRooms.length).toBe(2);
        expect(Object.keys(result.mapping).length).toBe(2);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });

    it('should create correct szallasHuRooms structure', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [
        {
          id: 1,
          szallas_hu_ext_room_id: 'szh-101',
          szallas_hu_ext_room_name: 'Test Room',
          vendegem_ext_room_id: 'vg-201',
          vendegem_ext_room_name: 'Test Vendégem Room',
          created_date: new Date()
        }
      ];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        expect(result.szallasHuRooms[0]).toEqual({
          id: 1,
          externalId: 'szh-101',
          name: 'Test Room'
        });
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });

    it('should create correct vendegemRooms structure', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [
        {
          id: 1,
          szallas_hu_ext_room_id: 'szh-101',
          szallas_hu_ext_room_name: 'Test Szállás Room',
          vendegem_ext_room_id: 'vg-201',
          vendegem_ext_room_name: 'Test Room',
          created_date: new Date()
        }
      ];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        expect(result.vendegemRooms[0]).toEqual({
          id: 1,
          externalId: 'vg-201',
          name: 'Test Room'
        });
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });

    it('should handle null vendegem fields when no mapping exists', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [
        {
          id: 1,
          szallas_hu_ext_room_id: 'szh-101',
          szallas_hu_ext_room_name: 'Unmapped Room',
          vendegem_ext_room_id: null,
          vendegem_ext_room_name: null,
          created_date: new Date()
        }
      ];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        expect(result.szallasHuRooms[0]).toEqual({
          id: 1,
          externalId: 'szh-101',
          name: 'Unmapped Room'
        });
        expect(result.vendegemRooms[0]).toEqual({
          id: 1,
          externalId: null,
          name: null
        });
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });

    it('should create correct mapping with string IDs', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [
        {
          id: 1,
          szallas_hu_ext_room_id: 'szh-101',
          szallas_hu_ext_room_name: 'Room 1',
          vendegem_ext_room_id: 'vg-201',
          vendegem_ext_room_name: 'Room 1',
          created_date: new Date()
        }
      ];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        expect(result.mapping['1']).toBe('1');
        expect(typeof result.mapping['1']).toBe('string');
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });

    it('should handle mixed mapped and unmapped rooms', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [
        {
          id: 1,
          szallas_hu_ext_room_id: 'szh-101',
          szallas_hu_ext_room_name: 'Mapped Room',
          vendegem_ext_room_id: 'vg-201',
          vendegem_ext_room_name: 'Vendégem Room',
          created_date: new Date()
        },
        {
          id: 2,
          szallas_hu_ext_room_id: 'szh-102',
          szallas_hu_ext_room_name: 'Unmapped Room',
          vendegem_ext_room_id: null,
          vendegem_ext_room_name: null,
          created_date: new Date()
        }
      ];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        expect(result.szallasHuRooms.length).toBe(2);
        expect(result.vendegemRooms.length).toBe(2);
        expect(result.vendegemRooms[0].externalId).toBe('vg-201');
        expect(result.vendegemRooms[1].externalId).toBeNull();
        expect(result.vendegemRooms[1].name).toBeNull();
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });

    it('should handle empty response', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        expect(result.szallasHuRooms.length).toBe(0);
        expect(result.vendegemRooms.length).toBe(0);
        expect(Object.keys(result.mapping).length).toBe(0);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });

    it('should maintain Room interface structure with nullable fields', (done) => {
      const accommodationId = 1;
      const mockResponse: MapRecord[] = [
        {
          id: 5,
          szallas_hu_ext_room_id: 'szh-500',
          szallas_hu_ext_room_name: 'Test',
          vendegem_ext_room_id: null,
          vendegem_ext_room_name: null,
          created_date: new Date()
        }
      ];

      service.listAccommoddationMappingConfiguration(accommodationId).subscribe(result => {
        const room = result.vendegemRooms[0];
        expect(room.id).toBe(5);
        expect(room.externalId).toBeNull();
        expect(room.name).toBeNull();
        expect(room).toEqual(jasmine.objectContaining({
          id: jasmine.any(Number),
          externalId: null,
          name: null
        }));
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/accommodations/${accommodationId}/mapping-configuration`);
      req.flush(mockResponse);
    });
  });

  describe('getEnumKey', () => {
    it('should return correct key for SZALLAS_HU', () => {
      const result = service.getEnumKey(ConnectionType.SZALLAS_HU);
      expect(result).toBe('SZALLAS_HU');
    });

    it('should return correct key for VENDEGEM', () => {
      const result = service.getEnumKey(ConnectionType.VENDEGEM);
      expect(result).toBe('VENDEGEM');
    });

    it('should return undefined for invalid value', () => {
      const result = service.getEnumKey('INVALID' as ConnectionType);
      expect(result).toBeUndefined();
    });
  })
});