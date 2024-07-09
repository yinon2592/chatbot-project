import React, { useState } from "react";
import { TextField, Button, Box, Typography, Paper } from "@mui/material";
import { ChatApi } from "../../api/api";
import { useMutation } from '@tanstack/react-query';
import './chat.css';

export const Chat: React.FC = () => {
    const [messages, setMessages] = useState<{ sender: 'you' | 'bot', text: string }[]>([]);
    const [inputValue, setInputValue] = useState("");  // State to hold the input value

    const {
        isSuccess: _isQuerySuccess,
        isError: _isQueryerror,
        isPending: isQueryPending,
        mutate: sendQuery,
      } = useMutation({
        retry: false,
        mutationFn: ChatApi.sendMessage,
        onSuccess: (data, _variables, _context) => {
            // console.log('Received data:', data);  // Debug log
            setMessages(prev => [...prev, { sender: 'bot', text: data }]);
            setInputValue("");  // Clear the input field after sending the message
        },
        onError: (error) => {
            console.log(error);
        },
      });

    const sendMessage = async () => {
        if (inputValue.trim()) {  // Check if the input value is not just empty spaces
            setMessages(prev => [...prev, { sender: 'you', text: inputValue }]);
            sendQuery(inputValue);
        }
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        sendMessage();
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);  // Update state with the input value
    };

    return (
        <Box className="chat-box" sx={{ minheight: 480, margin: 'auto', padding: 2, maxWidth: 800, backgroundColor: '#e7f7e7' }}>
            <Typography variant="h4" gutterBottom>Chatbot</Typography>
            <Paper style={{ maxHeight: 480, overflow: 'auto', padding: '20px', marginBottom: '20px', maxWidth: 800, backgroundColor: '#e7f7e7'}}>
                {messages.map((msg, index) => (
                    <Typography key={index} className={msg.sender === 'you' ? 'userMessage' : 'botMessage'}>
                        {msg.text}
                    </Typography>
                ))}
            </Paper>
            <form onSubmit={handleSubmit}>
                <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Type a message"
                    value={inputValue}  // Bind input value to state
                    onChange={handleInputChange}  // Update state when input changes
                    multiline
                    minRows={3}
                    onKeyDown={handleKeyDown}  
                    InputProps={{
                        endAdornment: (
                            <Button type="submit" variant="contained" color="primary" disabled={isQueryPending}>
                                Send
                            </Button>
                        )
                    }}
                />
            </form>
        </Box>
    );
};
