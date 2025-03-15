import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Custom Marvel styling

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("⚠️ Please select an image!");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setErrorMessage(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setAnalysis({
        ...response.data,
        seo_description: response.data.seo_description || "No description available.",
      });

    } catch (error) {
      console.error("Error analyzing image:", error);
      setErrorMessage("Something went wrong. Try again!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="upload-box">
        <h1>🦸 AI Image Analyzer</h1>
        <p>Upload an image & get AI-powered insights!</p>

        <input type="file" onChange={handleFileChange} className="file-input" />

        {preview && (
          <div className="preview-box">
            <img src={preview} alt="Uploaded Preview" />
          </div>
        )}

        <button onClick={handleUpload} disabled={loading} className="analyze-btn">
          {loading ? "🔍 Analyzing..." : "Analyze Image"}
        </button>

        {errorMessage && <p className="error-msg">{errorMessage}</p>}

        {analysis && (
          <div className="result-box">
            <h2>🔍 Image Analysis</h2>
            <p><b>Predictions:</b> {analysis.predictions}</p>
            <p><b>SEO Description:</b> {analysis.seo_description}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;








