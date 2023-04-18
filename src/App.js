import React, { useState } from 'react';
import axios from 'axios';
import { css } from '@emotion/react';
import { ClipLoader } from 'react-spinners';

const override = css`
  display: block;
  margin: 0 auto;
  border-color: #27ae60;
`;

function App() {
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    console.log("Generating Summary");
    const formData = new FormData();
    formData.append('audio', file);

    const response = await axios.post('http://localhost:5000/summarize', formData);
    setSummary(response.data.summary);
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="header">
        <h1 className="logo">Socratique Audio Summarizer</h1>
        <nav>
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Labs</a></li>
            <li><a href="#">Chatbot</a></li>
          </ul>
        </nav>
      </header>
      <main>
        <div className="form-container">
          <h2>Socratique - Summarise Audio</h2>
          <form onSubmit={onSubmit}>
            <div className="form-group">
              <label htmlFor="audio-file">Choose an audio file:</label>
              <input type="file" id="audio-file" className="button-blue" onChange={onFileChange} />
            </div>
            {file && !loading && <button type="submit" className="button-greenish">Summarize</button>}
            {file && loading && (
              <button type="submit" className="button-greenish" disabled>
                <ClipLoader color={'#fff'} loading={true} css={override} size={15} />
              </button>
            )}
          </form>
        </div>
        {summary && (
          <div className="summary">
            <h2>Summary:</h2>
            <p>{summary}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
