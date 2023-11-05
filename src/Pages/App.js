// React & Node Imports
import React from 'react';
import { useState } from 'react';

// Components & Styling Imports
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Container, Form} from 'react-bootstrap';
import CNavbar from '../Components/CNavbar';
import Output from '../Components/Output';
import './App.css';

export default function App(){

  // Set Initial States of Form Fields
  const [query,setQuery] = useState("");
  const [links,setLinks] = useState("");
  const [API,setAPI] = useState("");
  const [outputData,setOutputData] = useState(null);
  const [searched,SetSearched] = useState(false);

  // Handles Search
  const handleSearch = async() => {
    // Parse each link into an array
    const linksArr = links.split('\n').map(links => links.trim()).filter(links => links.length > 0);
    const request = `${API}?q=${query}&url=${linksArr[0]}`;
    console.log(request);
    try {
      const response = await fetch(request, {
        method: 'GET',
      });
  
      if (response.ok) {
        const jsonData = await response.json();
        setOutputData(jsonData);
      } else {
        console.error('API request failed');
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
    
    SetSearched(true);
  }

  console.log()

  return (
    <div className='base text-center'>
      <Container >
        <CNavbar/>

        <Container className='mt-5 mb-5 forms'>
          <Form>
            <Form.Group>
              <Form.Control
                type="text"
                id="SearchQuery"
                placeholder="Enter a one-line query"
                value={query}
                className='mb-3'
                onChange={(event) => setQuery(event.target.value)}/>
            </Form.Group>

            <Form.Group>
              <Form.Control
                as="textarea"
                id="URLlist"
                placeholder="Enter multiple URLs"
                value={links}
                className='mb-3'
                rows={4}
                onChange={(event) => setLinks(event.target.value)}/>
            </Form.Group>

            <Form.Group>
              <Form.Control
                type="text"
                id="SearchAPI"
                placeholder="Temporary API URL"
                value={API}
                className='mb-3'
                rows={4}
                onChange={(event) => setAPI(event.target.value)}/>
            </Form.Group>

            <Button 
              className={`search ${searched ? 'search-performed' : ''}`}
              onClick={handleSearch}>
              Search
            </Button>

          </Form>
        </Container>

        {searched && <Output data={outputData} className='mt-5 mb-5'/>}

      </Container>
    </div>
  );
}