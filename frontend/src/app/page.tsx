"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      alert(data.message);
    } catch (err) {
      alert("Upload failed!");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/ask?q=${encodeURIComponent(question)}`);
      const data = await res.json();
      setResponse(data.answer || data.summary || data.error);
    } catch {
      setResponse("Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>📄 GenAI PDF Processor</h1>

      <div className="upload-section">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload PDF</button>
      </div>

      <div className="query-section">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question or type 'Give me summary'"
        />
        <button onClick={handleAsk}>Ask</button>
      </div>

      {loading && (
        <div className="loader">
          <div className="spinner"></div>
          <p>Processing...</p>
        </div>
      )}

      {response && !loading && (
        <div className="response-box">
          <h3>🧠 Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
