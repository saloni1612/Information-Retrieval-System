import React, { useState } from 'react';

export default function ChatWidget() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = input;
    setMessages([...messages, { sender: 'user', text: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/query/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ question: userMessage })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { sender: 'bot', text: data.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Error: could not connect to server.' }]);
    }
    setLoading(false);
  };

  return (
    <div className="chat-widget">
      <h3>Product Chatbot</h3>
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.sender}>
            <strong>{msg.sender === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
          </div>
        ))}
        {loading && <p>Bot is typing...</p>}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about a product..." />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
