import { useMutation, useQueryClient } from '@tanstack/react-query';
import { OrderApi } from "../api/api";
import { toast } from 'react-toastify';

export const useDeleteOrder = () => {
    const queryClient = useQueryClient();

    const { 
        mutate: deleteOrder, 
        isPending
    } = useMutation({
        retry: false,
        mutationFn: OrderApi.deleteOrder,
        onSuccess: (data) => {
            toast.success('Order deleted successfully.');
            queryClient.invalidateQueries({ queryKey: ['getOrders']});
            queryClient.invalidateQueries({ queryKey: ['getOrder', data]});
        },
        onError: (error) => {
            console.error('Error deleting order:', error);
            toast.error('Failed to delete order.');
        },
    });

    return { deleteOrder, isPending };
};
