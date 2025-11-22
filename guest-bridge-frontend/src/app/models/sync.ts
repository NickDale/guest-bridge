export interface SyncDetail {
    id: number;
    reservation_id: string;
    debug_message: string; // Pl. "RoomMapping: 101 -> VGE-R1"
    error_message: string;
    status: string;
    type: SyncType;
    created_date: Date;
    created_by?: string;
}

export enum SyncType {
    FOGLALAS,
    LEMONDAS
}

export interface SyncRecord {
    id: number;
    accommodation_id: number;
    status: string;
    error_message: string;
    debug_message: string;
    created_date: Date;
    created_by?: string;
    details: SyncDetail[];
}