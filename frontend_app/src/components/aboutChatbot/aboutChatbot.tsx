import "./aboutChatbot.css"
import React from 'react';
import { Box, Typography } from '@mui/material';

export const AboutChatbot: React.FC = () => {
  return (
    <Box sx={{ padding: 2, marginBottom: 2 }}>
      <Typography variant="h5" gutterBottom>
        About the Chatbot
      </Typography>
      <Typography variant="body1">
        This educational chatbot helps with order status, return policies, and connecting with a human representative.<br />
        Just ask your question in the chat box below.
      </Typography>
    </Box>
  );
};
