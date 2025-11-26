export interface Address {
    id: number;
    name: string;
    email: string;
    tax: string;
    postcode: string;
    country: string;
    city: string;
    street: string;
    street_number: string;
    floor: string;
    door: string;
}

export interface AddressCreationRequest {
    postcode: string;
    country: string;
    city: string;
    street: string;
    street_number: string;
    floor: string | null;
    door: string | null;
}


export interface BillingAddressUpdate {
    id: number;
    name: string;
    email: string | null | undefined;
    tax: string | null | undefined;
    postcode: string | null | undefined;
    country: string;
    city: string | null | undefined;
    street: string | null | undefined;
    street_number: string | null | undefined;
    floor: string | null | undefined;
    door: string | null | undefined;
}
