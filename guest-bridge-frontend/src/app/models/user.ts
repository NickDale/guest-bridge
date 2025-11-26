import { Address, BillingAddressUpdate } from "./address";

export interface User {
    id: number;
    full_name: string;
    username?: string | null;
    email: string;
    status: string;
    type: string;
    subscription_type: string;
    activation_date: Date,
    blocked_date: Date,
    created_date: Date,
    number_of_accommodations: number;

    billing_info: Address;
}


export interface UpdateUserRequest {
    full_name: string;
    email: string;
    billing_info: BillingAddressUpdate;
}