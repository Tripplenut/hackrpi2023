// React Imports
import React from 'react';
import ReactDOM from 'react-dom/client';

// Styling Imports
import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css';

// Component & Page Imports
import App from './Pages/App.js';


const root = document.createElement('div');
root.className = 'container';
document.body.appendChild(root);
const rootDiv = ReactDOM.createRoot(root);

rootDiv.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);