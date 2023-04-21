import "./styles.css";


import React from 'react';
import { useState } from 'react';

function App() {
  const [imageSrc, setImageSrc] = useState('');

  const handleDetectImage = () => {
    //API which returns detected image
    const detectedImageUrl = 'https://picsum.photos/200/300';

    setImageSrc(detectedImageUrl);
  };

  return (
    <div>
      <button onClick={handleDetectImage}>Detect Image</button>
      {imageSrc && <img src={imageSrc} alt="Detected Image" />}
    </div>
  );
}

export default App;
