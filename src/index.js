// React Imports
import React from 'react';
import ReactDOM from 'react-dom/client';

// Styling Imports
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';

// Component & Page Imports
import App from './Pages/App.js';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>
);

