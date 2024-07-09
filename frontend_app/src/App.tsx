import './App.css'
import React from 'react'
import { AboutChatbot } from './components/aboutChatbot/aboutChatbot'
import { Chat } from './components/chat/chat'
import { OrderBox } from './components/orderBox/orderBox'
import { Box, Grid, Typography, Container } from '@mui/material'

const App: React.FC = () => {
  return (
    <Container>
      <Box sx={{ flexGrow: 1, padding: 2 }}>
        <Typography variant="h2" gutterBottom component="div" align="center" sx={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)' }}>
          Welcome to E-commerce Customer Support Chatbot
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <AboutChatbot />
          </Grid>
          <Grid item xs={12}>
            <Chat />
          </Grid>
          <Grid item xs={12}>
            <OrderBox />
          </Grid>
        </Grid>
      </Box>
    </Container>
  )
}

export default App
