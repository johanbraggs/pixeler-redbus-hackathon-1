import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:3000');

function ImageStream() {
  const [images, setImages] = useState([]);

  useEffect(() => {
    socket.on('imageSent', (imageData) => {
      setImages((prevImages) => [...prevImages, imageData]);
    });
  }, []);

  return (
    <div>
      {images.map((image, index) => (
        <img key={index} src={`data:image/jpeg;base64,${image}`} alt="Streamed Image" />
      ))}
    </div>
  );
}

export default ImageStream;
