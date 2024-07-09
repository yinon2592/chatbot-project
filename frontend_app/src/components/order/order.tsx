import { OrderData, OrderStatus } from "../../types";
import "./order.css";
import React, { useState } from 'react';
import { Button, Typography, Paper, Select, MenuItem, CircularProgress } from '@mui/material';
import { useDeleteOrder } from '../../hooks/useDeleteOrder'; // Adjust the path as needed
import { useUpdateOrder } from '../../hooks/useUpdateOrder'; // Adjust the path as needed

export const Order: React.FC<OrderData> = ({ id, orderStatus }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [newStatus, setNewStatus] = useState<OrderStatus>(orderStatus);

    const { deleteOrder, isPending: isDeleting } = useDeleteOrder();
    const { updateOrder, isPending: isUpdating } = useUpdateOrder();

    const handleDelete = () => {
        deleteOrder(id as string);
    };

    const handleUpdate = () => {
        updateOrder({ id, orderStatus: newStatus });
        setIsEditing(false);
    };

    return (
        <Paper sx={{ padding: 2, mt: 2 }}>
            <Typography><strong>Order ID:</strong> {id}</Typography>
            {isEditing ? (
                <>
                    <Select
                        label="Order Status"
                        value={newStatus}
                        onChange={(e) => setNewStatus(e.target.value as OrderStatus)}
                        fullWidth
                        margin="dense"
                    >
                        <MenuItem value="Pending">Pending</MenuItem>
                        <MenuItem value="Delivered">Delivered</MenuItem>
                        <MenuItem value="Cancelled">Cancelled</MenuItem>
                    </Select>
                    <Button 
                        variant="contained" 
                        color="primary" 
                        onClick={handleUpdate} 
                        sx={{ mt: 2 }} 
                        disabled={isUpdating}
                    >
                        {isUpdating ? <CircularProgress size={24} /> : 'Save'}
                    </Button>
                    <Button 
                        variant="outlined" 
                        color="secondary" 
                        onClick={() => setIsEditing(false)} 
                        sx={{ mt: 2, ml: 2 }}
                    >
                        Cancel
                    </Button>
                </>
            ) : (
                <>
                    <Typography><strong>Status:</strong> {orderStatus}</Typography>
                    <Button 
                        variant="outlined" 
                        color="primary" 
                        onClick={() => setIsEditing(true)} 
                        sx={{ mt: 2 }}
                    >
                        Edit
                    </Button>
                    <Button 
                        variant="contained" 
                        color="secondary" 
                        onClick={handleDelete} 
                        sx={{ mt: 2, ml: 2 }} 
                        disabled={isDeleting}
                    >
                        {isDeleting ? <CircularProgress size={24} /> : 'Delete'}
                    </Button>
                </>
            )}
        </Paper>
    );
};
