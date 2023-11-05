import React from 'react';
import { Container } from "react-bootstrap";
import "./Output.css"

/** Data = An Object
 * Data.similarity - int = Similarity of text to query
 * Data.url - string = The url
 * Data.text - string = The text
 */
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
            href={info.url}>
            {info.url} 
          </a>

          <p>{info.text}</p>

        </div>
      ))}

    </Container>
  );
}