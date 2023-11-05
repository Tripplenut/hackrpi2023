import { Container } from "react-bootstrap";
import "./Output.css"

// Data = A json array of tuple
export default function Output({data}){

  return (
    <Container>
      <h1 className="title">
        Output
      </h1>

      {data.map((info, index) => (
        <div key={index} className="fields mb-3">

          <a
            className='links'
            href={info[1]}>
            {info[1]} 
          </a>

          <p>{info[0]}</p>

        </div>
      ))}

    </Container>
  );
}