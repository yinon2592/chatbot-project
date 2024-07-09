import "./updateOrder.css";
import React, { useState } from 'react';
import { TextField, Button, Box, Typography, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { toast } from 'react-toastify';
import { OrderStatus } from '../../types';
import { SelectChangeEvent } from '@mui/material/Select';
import { useUpdateOrder } from '../../hooks/useUpdateOrder';

export const UpdateOrder: React.FC = () => {
    const [orderId, setOrderId] = useState('');
    const [orderStatus, setOrderStatus] = useState<OrderStatus>('Pending');

    const { updateOrder, isPending } = useUpdateOrder();

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setOrderId(event.target.value);
    };

    const handleStatusChange = (event: SelectChangeEvent) => {
        setOrderStatus(event.target.value as OrderStatus);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (orderId && orderStatus) {
            updateOrder({ id: orderId, orderStatus: orderStatus });
        } else {
            toast.error('Please enter both Order ID and Status.');
        }
    };

    return (
        <Box sx={{ maxWidth: 480, margin: 'auto', padding: 2 }}>
            <Typography variant="h4" gutterBottom component="div">
                Update Order Status
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
                <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }} disabled={isPending}>
                    Update Order Status
                </Button>
            </form>
        </Box>
    );
};
