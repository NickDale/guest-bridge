import { Address } from "./address";

export interface User {
    id: number;
    full_name: string;
    username:string;
    email: string;
    status:string;
    type: string;
    subscription_type:string;
    activation_date:Date,
    blocked_date:Date,
    created_date:Date,
    numberOfAccommodations:number;


    billing_info:Address;
}