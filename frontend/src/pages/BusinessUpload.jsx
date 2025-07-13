// src/pages/BusinessUpload.jsx
import React, { useState } from 'react';
import './BusinessUpload.css';

function BusinessUpload() {
  const [businessName, setBusinessName] = useState('');
  const [businessType, setBusinessType] = useState('');
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('business', businessName);
    formData.append('type', businessType);

    try {
      const res = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setMessage(data.message || 'Uploaded successfully');
    } catch (err) {
      console.error(err);
      setMessage('Upload failed');
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Business Catalog</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <input
          type="text"
          placeholder="Business Name"
          value={businessName}
          onChange={(e) => setBusinessName(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Business Type"
          value={businessType}
          onChange={(e) => setBusinessType(e.target.value)}
          required
        />

        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />

        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default BusinessUpload;
