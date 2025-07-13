import React, { useState } from 'react';
import './UserBrowse.css';

const UserBrowse = () => {
  const [businesses] = useState([
    { name: 'CakeCo', type: 'Bakery' },
    { name: 'PaperNest', type: 'Packaging' },
  ]);
  const [selectedBusiness, setSelectedBusiness] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleAsk = async () => {
    if (!selectedBusiness || !question) {
      alert('Please select a business and enter a question.');
      return;
    }

    const response = await fetch('http://localhost:8000/query/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: question,
        business: selectedBusiness,
      }),
    });

    const data = await response.json();
    setAnswer(data.answer || 'No response received.');
  };

  return (
    <div className="user-chat-container">
      <h2>Ask a Business</h2>
      <select
        value={selectedBusiness}
        onChange={(e) => setSelectedBusiness(e.target.value)}
      >
        <option value="">Select business</option>
        {businesses.map((b, idx) => (
          <option key={idx} value={b.name}>
            {b.name} ({b.type})
          </option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Ask your question here"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={handleAsk}>Ask</button>

      {answer && (
        <div className="response">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default UserBrowse;
