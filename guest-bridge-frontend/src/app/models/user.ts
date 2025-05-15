export interface User {
    id: number;
    full_name: string;
    username:string;
    email: string;
    status:string;
    subscriptionType:string;
    numberOfAccommodations:number;

    //TODO: replace with address
    billingAddress:string;
}