import axios from 'axios';
import { OrderData } from '../types';
import io from 'socket.io-client';
import {
    ORDER_PATH,
    ORDERS_PATH,
    ORDER_ID_PATH,
}from '../constants'


const apiDevUrl =  'http://localhost:5000';
const apiProdUrl = 'https://chatbot-project-1jej.onrender.com/'

const baseUrl = process.env.NODE_ENV === 'production' ? apiProdUrl : apiDevUrl;
const socket = io(baseUrl);

socket.on('connect', () => {
    console.log('Connected to server');
    console.log('Socket ID:', socket.id); 
});

const api = axios.create({
  baseURL: baseUrl, 
});

const LIMIT = 10;

export const ChatApi = {
    sendMessage: (message: string): Promise<string> => {
        return new Promise((resolve, reject) => {
            socket.emit('chat', { message: message, room: socket.id});

            socket.on('bot_response', data => {
                resolve(data.response);
            });

            socket.on('connect_error', (err) => {
                reject('Connection Failed: ' + err.message);
            });
        });
    },
};

export const OrderApi = {

    createOrder: async (order: OrderData): Promise<string> => { // return order id
        const response = await api.post(ORDER_PATH, { status: order.orderStatus });        
        return response.data.id;
    },

    getOrder: async (orderId: string): Promise<OrderData> => {
        const response = await api.get(ORDER_ID_PATH.replace(':orderId', orderId));
        return response.data;
    },

    getOrders: async ({ pageParam } : { pageParam: string | null }): Promise<{
        data: OrderData[];
        currentPage: string | null;
        nextPage: string | null;
    }> => {
        const response = await api.get(ORDERS_PATH, {
            params: {
                lastKey: pageParam, 
                limit: LIMIT, 
            },
        });
    
        const data = response.data.items as OrderData[];
        const currentPage = pageParam;
        const nextPage = response.data.lastEvaluatedKey ? response.data.lastEvaluatedKey.id : null;
        
        return { data, currentPage, nextPage };
    },

    updateOrder: async ({id, orderStatus}: OrderData): Promise<void> => {
        const response = await api.put(ORDER_ID_PATH.replace(':orderId', id as string), {orderStatus});
        return response.data.id;
    },

    deleteOrder: async (orderId: string): Promise<void> => {
        const response = await api.delete(ORDER_ID_PATH.replace(':orderId', orderId));
        return response.data.id;
    }
};
