import "./deleteOrder.css";
import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import { toast } from 'react-toastify';
import { useDeleteOrder } from '../../hooks/useDeleteOrder';

export const DeleteOrder: React.FC = () => {
    const [orderId, setOrderId] = useState('');

    const { deleteOrder, isPending } = useDeleteOrder();

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setOrderId(event.target.value);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (orderId) {
            deleteOrder(orderId);
        } else {
            toast.error('Please enter an order ID.');
        }
    };

    return (
        <Box sx={{ maxWidth: 480, margin: 'auto', padding: 2 }}>
            <Typography variant="h4" gutterBottom component="div">
                Delete Order
            </Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Order ID"
                    variant="outlined"
                    value={orderId}
                    onChange={handleInputChange}
                    fullWidth
                    margin="normal"
                    placeholder="Enter valid order ID"
                />
                <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }} disabled={isPending}>
                    Delete Order
                </Button>
            </form>
        </Box>
    );
};
