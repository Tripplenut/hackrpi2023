import { Navbar, Container } from 'react-bootstrap';

export default function CNavbar(){
  return (
    <Navbar bg="dark" variant="dark" expand="lg" style={{ borderRadius: '10px' }}>
      <Container>
        <Navbar.Brand href="#">Google++</Navbar.Brand>
      </Container>
    </Navbar>
  );
}