import React from 'react';
import "./index.css";

function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height:'100%' }}>
      <h1>What type of investor are you?</h1>
      <div className = "allElems">
        <button className='buttons'>I want to invest in something safe</button>
        <button className='buttons'>High risk, high reward</button>
      </div>
    </div>
  );
}

export default App;