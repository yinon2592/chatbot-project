export type OrderStatus =  'Pending' | 'Delivered' | 'Cancelled';

export interface OrderData {
    id?: string;
    orderStatus: OrderStatus;
}

// Contact information should include full name, email, and phone number
export interface ContactInfo {
    fullName: string;
    email: string;
    phoneNumber: string;
}