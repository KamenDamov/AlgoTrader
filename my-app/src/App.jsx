import React from 'react';
import "./index.css";

function App() {
  return (
    <div class = "allElems">
      <h1>What type of investor are you?</h1>
      <div>
        <button className='buttons'>I want to invest in something safe</button>
        <button className='buttons'>High risk, high reward</button>
      </div>
    </div>
  );
}

export default App;