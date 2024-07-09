import "./orderBox.css";
import React from 'react';
import { NewOrder } from "../newOrder/newOrder";
import { GetOrder } from "../getOrder/getOrder";
import { GetOrders } from "../getOrders/getOrders";
import { UpdateOrder } from "../updateOrder/updateOrder";
import { DeleteOrder } from "../deleteOrder/deleteOrder";
import { Box, Grid, Typography, Paper } from '@mui/material';

export const OrderBox: React.FC = () => {
    return (
        <Box sx={{ flexGrow: 1, padding: 2 }}>
        <Typography variant="h4" gutterBottom component="div" align="center">
          Order Management
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={3}
                  sx={{ padding: 2, backgroundColor: '#f0f4c3', borderRadius: 2, boxShadow: 3 }}
                >
                  <NewOrder />
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={3}
                  sx={{ padding: 2, backgroundColor: '#ffecb3', borderRadius: 2, boxShadow: 3 }}
                >
                  <GetOrder />
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={3}
                  sx={{ padding: 2, backgroundColor: '#b3e5fc', borderRadius: 2, boxShadow: 3 }}
                >
                  <UpdateOrder />
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={3}
                  sx={{ padding: 2, backgroundColor: '#c8e6c9', borderRadius: 2, boxShadow: 3 }}
                >
                  <DeleteOrder />
                </Paper>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12}>
            <Paper
              elevation={3}
              sx={{ padding: 2, backgroundColor: '#bbdefb', borderRadius: 2, boxShadow: 3 }}
            >
              <GetOrders />
            </Paper>
          </Grid>
        </Grid>
      </Box>
      
    );
};
