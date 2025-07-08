import { useState } from "react";
import { storage } from "../lib/appwrite";

export default function Home() {
  const [file, setFile] = useState(null);

  const uploadAndSend = async () => {
    const uploaded = await storage.createFile("bucket_id", "unique()", file);
    const url = storage.getFilePreview("bucket_id", uploaded.$id).href;

    await fetch("http://localhost:8000/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file_url: url }),
    });
  };

  return (
    <div>
      <h1>GenAI PDF Uploader</h1>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={uploadAndSend}>Upload & Process</button>
    </div>
  );
}
