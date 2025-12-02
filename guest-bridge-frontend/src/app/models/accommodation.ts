import { Address, AddressCreationRequest } from "./address";

export interface Accomodation {
    id: number;
    name: string;
    address: string;
    active: boolean;
    numberOfPlaces: number;
}

export interface AccomodationDetail {
    id: number;
    name: string;
    status: string;
    address: Address;
    szallas_hu: ExternalConnection;
    vendegem: ExternalConnection;
    contact_name: string;
    contact_phone: string;
    contact_email: string;
    reg_number: string;
    created_date: Date;
}

export interface ExternalConnection {
    id: string;
    ref: string;
}

export interface AccommodationCreationRequest {
    name: string
    user_id: number
    ntak_no: string
    vendegem_id?: string
    szallas_hu_id?: string
    vendegem_ref?: string
    contact_name?: string
    contact_phone?: string
    contact_email?: string
    address: AddressCreationRequest
}