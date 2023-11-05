import { useState } from 'react';
import { Button, Container, Form} from 'react-bootstrap';
import CNavbar from '../Components/CNavbar';
import Output from '../Components/Output';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

export default function App(){

  // Set Initial States of Form Fields
  const [query,setQuery] = useState("");
  const [links,setLinks] = useState("");
  const [searched,SetSearched] = useState(false);

  // Handles Search
  const handleSearch = () => {
    // Parse each link into an array
    const linksArr = links.split('\n').map(links => links.trim()).filter(links => links.length > 0);

    // Create JS Object
    const obj = {
      Query: query,
      Links: linksArr,
    }

    // Convert object to string
    const json = JSON.stringify(obj)

    //Temporary
    console.log(json)
    SetSearched(true);
  } 

  const jsonData = [
    [
    "GitHub is a platform for developers to collaborate, host, and review code. It's a hub for open-source projects and a valuable resource for version control and project management in the programming world."
    ,"https://github.com"
    ],
    [
    "Stack Overflow is a Q&A platform where programmers can ask questions and get answers from the developer community. It's an invaluable resource for troubleshooting coding issues and learning from others' experiences."
    ,"https://stackoverflow.com"
    ],
    ["Spotify is a popular music streaming service. With a vast library of songs and personalized playlists, it's perfect for music enthusiasts like you. You can explore and discover new tunes while enjoying your favorite tracks."
    ,"https://www.spotify.com"],
    ["Steam is a leading platform for PC gaming. You can buy, download, and play a wide range of video games, from indie titles to AAA blockbusters. It's a gamer's paradise."
    ,"https://store.steampowered.com"],
  ];

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

            <Button 
              className={`search ${searched ? 'search-performed' : ''}`}
              onClick={handleSearch}>
              Search
            </Button>

          </Form>
        </Container>

        {searched && <Output data={jsonData} className='mt-5 mb-5'/>}
        

      </Container>
    </div>
  );
}