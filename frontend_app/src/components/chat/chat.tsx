import React, { useEffect, useState } from "react";
import { TextField, Button, Box, Typography, Paper } from "@mui/material";
import { ChatApi } from "../../api/api";
import { useMutation } from '@tanstack/react-query';
import './chat.css';

export const Chat: React.FC = () => {
    const [messages, setMessages] = useState<{ sender: 'user' | 'assistant', text: string }[]>([]);
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
            setMessages(prev => [...prev, { sender: 'assistant', text: data }]);
            setInputValue("");  // Clear the input field after sending the message
        },
        onError: (error) => {
            console.log(error);
        },
      });

    const formatLastKMessages = (messages : { sender: 'user' | 'assistant', text: string }[], contextLength: Number) => {
        const lastMessages = messages.slice(-contextLength, -1);
        let formattedMessages = lastMessages.map(msg => `${msg.sender}: ${msg.text}`).join('\n');
        formattedMessages += `\ncurrent user message: ${messages[messages.length - 1].text}`;
        return formattedMessages;
    };

    const sendMessage = async () => {
        if (inputValue.trim()) {  // Check if the input value is not just empty spaces
            setMessages(prev => [...prev, { sender: 'user', text: inputValue }]);
        }
    };

    useEffect(() => {
        if (messages.length === 0 || messages[messages.length - 1].sender !== 'user') {
            return; // Don't run on initial render or if the last message isn't from the user
        }
    
        // Assuming formattedLastKMessages takes the whole messages array and formats the last 10 messages
        const formattedContext = formatLastKMessages(messages, 21);
        console.log("formattedContext:\n" + formattedContext);
    
        // Send both the latest message and the context
        sendQuery(formattedContext);
    
    }, [messages]);

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        sendMessage();
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter' && !event.shiftKey && !isQueryPending) {
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
                    <Typography key={index} className={msg.sender === 'user' ? 'userMessage' : 'assistantMessage'}>
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
