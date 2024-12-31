const http = require('http');

const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  let data = '';

  // Read incoming data in chunks
  req.on('data', chunk => {
    data += chunk;
  });

  // Once data is received, send it back as response
  req.on('end', () => {
	console.log(`Received data: ${data}`);
    res.writeHead(200, { 'Content-Type': 'application/JSON' });
    res.end(data);
  });
});

server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
