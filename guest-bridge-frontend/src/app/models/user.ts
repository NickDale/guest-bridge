export interface User {
    id: number;
    full_name: string;
    username:string;
    email: string;
    active:boolean;
    subscriptionType:string;
    numberOfAccommodations:number;

    //TODO: replace with address
    billingAddress:string;
}