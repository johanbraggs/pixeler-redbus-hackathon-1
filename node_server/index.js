// Import required packages
const express = require('express');
const http = require('http');
const cors = require('cors');

// Initialize the Express app
const app = express();

// Enable CORS
const corsOptions = {
  origin: 'http://localhost:5173',
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));


const server = http.createServer(app);
// const socketIO = require('socket.io')
const mongoose = require('mongoose');



// Initialize the Socket.IO server
const io = require('socket.io')(server, {
  cors: {
    origin: 'http://localhost:5173',
    methods: ['GET', 'POST']
  }
});

// Connect to the MongoDB database using Mongoose
mongoose.connect('mongodb+srv://anjuman:112311@devcluster.zr1azqg.mongodb.net/pixelar?retryWrites=true&w=majority', { useNewUrlParser: true });

// Define a schema for the data
const dataSchema = new mongoose.Schema({
  value: Number,
  timestamp: Date
});

// Create a model for the data
const Data = mongoose.model('Data', dataSchema);

// Listen for incoming Socket.IO connections
io.on('connection', (socket) => {
  console.log('New client connected =>', socket.id);

  // Listen for incoming data streams
  socket.on('data', (data) => {
    console.log('Received data:', data);

    // Save the data to the database
    const newData = new Data({
      value: data,
      timestamp: new Date()
    });
    newData.save();

    // Broadcast the data to all connected clients
    io.emit('dataSent', newData);
    console.log('Broadcasting data:', newData);
  });

  // Listen for client disconnection
  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

// Define an API endpoint to stream the saved data
app.get('/data', async (req, res) => {
  try {
    // Query the database for the saved data
    const data = await Data.find();
    // Stream the data as a JSON response
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Transfer-Encoding', 'chunked');
    res.flushHeaders();

    for (const item of data) {
      res.write(JSON.stringify(item));
      res.write('\n');
    }
    res.end();
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal Server Error' });
  }
});

// Start the server
const port = 3000;
server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
