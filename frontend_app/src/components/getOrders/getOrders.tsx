import "./getOrders.css"
import React from 'react';
import { useInfiniteQuery } from '@tanstack/react-query';
import { OrderApi } from "../../api/api";
import { Button, Box, Typography, CircularProgress } from '@mui/material';
import { Order } from "../order/order";

export const GetOrders: React.FC = () => {

    const {
        data: ordersPages,
        isLoading: isLoadingOrders,
        isError: isErrorGettingOrders,
        error: _getOrdersError,
        hasNextPage: hasNextOrders,
        fetchNextPage: fetchNextOrders,
        isFetchingNextPage: _isFetchingNextOrders,
    } = useInfiniteQuery({
            queryKey: ['getOrders'],
            queryFn: OrderApi.getOrders,
            initialPageParam: null,
            getNextPageParam: (lastPage) => lastPage.nextPage,
            retry: false,
            enabled: true,
    });

    const handleLoadMore = () => {
        if (hasNextOrders) {
            fetchNextOrders();
        }
    };

    return (
        <Box sx={{ maxWidth: 800, margin: 'auto', padding: 2, backgroundColor: '#f5f5f5', borderRadius: 2, boxShadow: 3 }}>
            <Typography variant="h4" gutterBottom component="div">
                Orders
            </Typography>
            {isLoadingOrders && (
                <Box display="flex" justifyContent="center" alignItems="center">
                    <CircularProgress />
                </Box>
            )}
            {isErrorGettingOrders && (
                <Typography color="error">
                    Error fetching the orders. Please try again.
                </Typography>
            )}
            {ordersPages && ordersPages.pages.map((page, pageIndex) => (
                <React.Fragment key={pageIndex}>
                    {page.data.map((order) => (
                        <Order key={`order-${order.id}`} {...order} />
                    ))}
                </React.Fragment>
            ))}
            {hasNextOrders && (
                <Button onClick={handleLoadMore} variant="contained" color="primary" sx={{ mt: 2 }} disabled={isLoadingOrders}>
                    Load More
                </Button>
            )}
        </Box>
    );
}
