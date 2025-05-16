import { Address } from "./address";

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