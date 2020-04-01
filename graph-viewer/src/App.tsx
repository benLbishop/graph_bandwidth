import React from 'react';
import logo from './logo.svg';
import './App.css';
import Graph from './components/Graph';

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <p>Graph of Bytes to and from Server over time</p>
      <Graph/>
      </header>
    </div>
  );
}

export default App;
