import React, { useState } from 'react';
import "./index.css";

function App() {
  const [text, setText] = useState('');

  return (
    <div class="allElems">
      <h1>What type of investor are you?</h1>
      <div class = "button-container">
        <button class='buttons' onMouseEnter={() => setText('You are a safe investor that would like to get a slow but steady return on investment')} 
                                onMouseLeave={() => setText('')}>I want to invest in something safe</button>

        <button class='buttons'onMouseEnter={() => setText('You are an aggressive investor and would like to have a big return on investment even though it is risky')} 
                                onMouseLeave={() => setText('')}>High risk, high reward</button>
        <p>{text}</p>
      </div>
    </div>
  );
}

export default App;