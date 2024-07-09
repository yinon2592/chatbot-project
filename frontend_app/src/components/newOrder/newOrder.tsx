import './newOrder.css';
import React, { useState } from 'react';
import { FormControl, InputLabel, Select, MenuItem, Button, Box, Typography, Paper } from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { OrderApi } from "../../api/api";
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { OrderStatus } from '../../types';
import { toast } from 'react-toastify';

export const NewOrder: React.FC = () => {
    const [orderStatus, setOrderStatus] = useState<OrderStatus>('Pending');
    const [orderId, setOrderId] = useState('');

    const queryClient = useQueryClient();

    const {
        isSuccess: _isOrderSuccess,
        isError: _isOrdererror,
        isPending: isOrderPending,
        mutate: createOrder,
      } = useMutation({
        retry: false,
        mutationFn: OrderApi.createOrder,
        onSuccess: (data, _variables, _context) => {
            console.log('Received data:', data);  // Debug log
            queryClient.invalidateQueries({ queryKey: ['getOrders']});
            queryClient.invalidateQueries({ queryKey: ['getOrder', data]});
            setOrderId(data);
        },
        onError: (error) => {
            console.log(error);
            toast.error('Failed to create order', { autoClose: 2000 });
        },
      });

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log('Order Status:', orderStatus); // Debug log
        createOrder({ orderStatus });
    };

    const handleStatusChange = (event: SelectChangeEvent) => {
        setOrderStatus(event.target.value as OrderStatus);
    };
    return (
        <Box sx={{ maxWidth: 480, margin: 'auto', padding: 2 }}>
            <Typography variant="h4" gutterBottom component="div">
                New Order
            </Typography>
            <form onSubmit={handleSubmit}>
                <FormControl fullWidth margin="normal">
                    <InputLabel id="order-status-label">Order Status</InputLabel>
                    <Select
                        labelId="order-status-label"
                        id="order-status"
                        value={orderStatus}
                        label="Order Status"
                        onChange={handleStatusChange}
                    >
                        <MenuItem value="Pending">Pending</MenuItem>
                        <MenuItem value="Delivered">Delivered</MenuItem>
                        <MenuItem value="Cancelled">Cancelled</MenuItem>
                    </Select>
                </FormControl>
                <Button type="submit" variant="contained" color="primary" disabled={isOrderPending}>
                    Create Order
                </Button>
            </form>
            <Paper elevation={3} sx={{ mt: 2, p: 2, minHeight: '50px' }}>
                    <Typography variant="h6">
                        Last Order ID: {orderId || "N/A"}
                    </Typography>
            </Paper>
        </Box>
    );
};