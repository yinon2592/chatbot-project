export type OrderStatus =  'Pending' | 'Delivered' | 'Cancelled';

export interface OrderData {
    id?: string;
    orderStatus: OrderStatus;
}