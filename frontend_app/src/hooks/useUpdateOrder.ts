import { useMutation, useQueryClient } from '@tanstack/react-query';
import { OrderApi } from "../api/api";
import { toast } from 'react-toastify';

export const useUpdateOrder = () => {
    const queryClient = useQueryClient();

    const { 
        mutate: updateOrder,
        isPending, 
    } = useMutation({
        retry: false,
        mutationFn: OrderApi.updateOrder,
        onSuccess: (data) => {
            toast.success("Order status updated successfully.");
            queryClient.invalidateQueries({ queryKey: ['getOrders']});
            queryClient.invalidateQueries({ queryKey: ['getOrder', data]});
        },
        onError: (error) => {
            console.log(error);
            toast.error('Failed to update order status.');
        },
    });

    return { updateOrder, isPending };
};
