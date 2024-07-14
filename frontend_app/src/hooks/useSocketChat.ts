import { useEffect, useState } from "react";
import { socket } from "../api/api";  // Adjust the import path as necessary

function useSocketChat() {
    const [messages, setMessages] = useState<{ sender: 'user' | 'assistant', text: string }[]>([]);
    const [isQueryPending, setIsQueryPending] = useState(false);

    useEffect(() => {
        const handleBotResponse = (data: { response: string }) => {
            setMessages(prev => [...prev, { sender: 'assistant', text: data.response }]);
            setIsQueryPending(false);  // Reset query pending flag after receiving response
        };

        const handleConnectError = (err: { message: string }) => {
            console.log('Connection Failed:', err.message);
            setIsQueryPending(false);  // Reset query pending flag on connection error
        };

        socket.on('bot_response', handleBotResponse);
        socket.on('connect_error', handleConnectError);

        // Clean up the event listeners when the component unmounts
        return () => {
            socket.off('bot_response', handleBotResponse);
            socket.off('connect_error', handleConnectError);
        };
    }, []);

    return { messages, setMessages, isQueryPending, setIsQueryPending };
}

export default useSocketChat;
