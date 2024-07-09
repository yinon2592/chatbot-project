import "./getOrder.css"
import React, { useState } from 'react';
import { OrderApi } from "../../api/api";
import { useQuery } from '@tanstack/react-query';
import { TextField, Button, Box, Typography, CircularProgress, Paper } from '@mui/material';
import { toast } from 'react-toastify';

export const GetOrder: React.FC = () => {
    const [orderId, setOrderId] = useState('');

    const {
        data: order,
        isLoading: isLoadingOrder,
        isError: isErrorOrder,
        refetch,
    } = useQuery({
        queryKey: ['getOrder', orderId],
        queryFn: () => OrderApi.getOrder(orderId),
        retry: false,
        enabled: false,  // Disable automatic execution
    });

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setOrderId(event.target.value);
    };

    const handleFetchOrder = () => {
        if (orderId) {
            refetch();
        } else {
            toast.error('Please enter an order ID.', { autoClose: 2000 });
        }
    };

    return (
        <Box sx={{ maxWidth: 480, margin: 'auto', padding: 2 }}>
            <Typography variant="h4" gutterBottom component="div">
                Get Order Status
            </Typography>
            <TextField
                label="Order ID"
                variant="outlined"
                value={orderId}
                onChange={handleInputChange}
                fullWidth
                margin="normal"
                placeholder="Enter a valid order ID"
            />
            <Button onClick={handleFetchOrder} variant="contained" color="primary" sx={{ mt: 2 }}>
                Get Order Status
            </Button>
            <Box sx={{ mt: 2 }}>
                {isLoadingOrder && (
                    <Box display="flex" justifyContent="center" alignItems="center">
                        <CircularProgress />
                    </Box>
                )}
                {isErrorOrder && (
                    <Typography color="error">
                        Error fetching order status, make sure to enter a valid order ID.
                    </Typography>
                )}
                {order && !isErrorOrder &&(
                    <Paper sx={{ padding: 2, mt: 2 }}>
                        <Typography variant="h6">Order Details</Typography>
                        <Typography><strong>Order ID:</strong> {order.id}</Typography>
                        <Typography><strong>Status:</strong> {order.orderStatus}</Typography>
                    </Paper>
                )}
            </Box>
        </Box>
    );
}
