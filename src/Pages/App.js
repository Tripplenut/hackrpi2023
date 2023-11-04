import { useState } from 'react';
import { Button, Container, Form} from 'react-bootstrap';
import CNavbar from '../Components/CNavbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'

export default function App(){

  const [query,setQuery] = useState("");
  const [links,SetLinks] = useState("");

  return (
    <div className='base text-center'>
      <Container >
        <CNavbar/>

        <Container className='mt-5 forms'>

          <Form>
            <Form.Group>
              <Form.Control
                type="text"
                placeholder="Enter a one-line query"
                className='mb-3'/>
            </Form.Group>

            <Form.Group>
              <Form.Control
                as="textarea"
                placeholder="Enter multiple URLs"
                className='mb-3'
                rows={4} />
            </Form.Group>

            <Button className='search'>
              Search
            </Button>

          </Form>

        </Container>
      </Container>
    </div>
  );
}