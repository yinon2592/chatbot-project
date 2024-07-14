import React, { useEffect, useState } from "react";
import { TextField, Button, Box, Typography, Paper } from "@mui/material";
import './chat.css';
import { socket } from "../../api/api";
import { formatLastKMessages } from "../../utils";
import  useSocketChat  from "../../hooks/useSocketChat";

export const Chat: React.FC = () => {
    const { messages, setMessages, isQueryPending, setIsQueryPending } = useSocketChat();
    const [inputValue, setInputValue] = useState("");  // State to hold the input value

    const sendMessage = async () => {
        if (inputValue.trim()) {  // Check if the input value is not just empty spaces
            setMessages(prev => [...prev, { sender: 'user', text: inputValue }]);
            setInputValue("");
            setIsQueryPending(true);
        }
    };

    useEffect(() => {
        if (messages.length === 0 || messages[messages.length - 1].sender !== 'user') {
            return; // Don't run on initial render or if the last message isn't from the user
        }
        const formattedContext = formatLastKMessages(messages, 21);
        console.log("formattedContext:\n" + formattedContext);
        socket.emit('chat', { message: formattedContext, room: socket.id});
        // socket.volatile.emit('chat', { message: formattedContext, room: socket.id});
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
