export const formatLastKMessages = (messages : { sender: 'user' | 'assistant', text: string }[], contextLength: Number) => {
    const lastMessages = messages.slice(-contextLength, -1);
    let formattedMessages = lastMessages.map(msg => `${msg.sender}: ${msg.text}`).join('\n');
    formattedMessages += `\ncurrent user message: ${messages[messages.length - 1].text}`;
    return formattedMessages;
};