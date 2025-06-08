import { useEffect, useState } from 'react';

function App() {
  const [response, setResponse] = useState('Loading...');

  useEffect(() => {
    fetch('http://localhost:8000/test')
      .then((res) => res.text()) // Use .json() if your API returns JSON
      .then((data) => setResponse(data))
      .catch((err) => setResponse('Error fetching data: ' + err.message));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>Welcome to Database Playground</h1>
      <p>Response from <code style={{color: 'lightblue'}}>backend/test</code>:</p>
      <pre style={{marginLeft: 2+'em', color: 'lightgreen'}}>{response}</pre>
    </div>
  );
}

export default App;
