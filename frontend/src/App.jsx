import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [chatLog, setChatLog] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const userMessage = { type: 'user', text: input };
    setChatLog([...chatLog, userMessage]); // Add user's message to log

    try {
      // This is the API call to your Python backend!
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      // The backend returns the full entry, we just want the ai_response
      const aiMessage = { type: 'ai', text: data.ai_response };
      setChatLog(prevLog => [...prevLog, aiMessage]); // Add AI's response

    } catch (error) {
      console.error('Error fetching data:', error);
      const errorMessage = { type: 'ai', text: 'Sorry, I ran into an error. Please try again.' };
      setChatLog(prevLog => [...prevLog, errorMessage]);
    }

    setInput(''); // Clear input box
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>EchoMind 🧠✨</h1>
        <p>Your AI-Powered Emotional Co-Pilot</p>
      </header>

      <div className="chat-window">
        {chatLog.length === 0 && (
          <div className="chat-message ai-message">
            <p>Hello! How are you feeling today? Write down your thoughts.</p>
          </div>
        )}
        {chatLog.map((message, index) => (
          <div key={index} className={`chat-message ${message.type}-message`}>
            <p>{message.text}</p>
          </div>
        ))}
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="How are you feeling...?"
        />
        <button type="submit">Send 🚀</button>
      </form>
    </div>
  );
}

export default App;