async function sendPrompt(prompt) {
  const response = await fetch('http://localhost:63343/submit_prompt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ prompt: prompt })
  });
  const data = await response.json();
  console.log(data); // Logs the response from the server
}

// Example usage:
sendPrompt('This is a test prompt.');
