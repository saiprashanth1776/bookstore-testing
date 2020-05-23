import React, { useState } from 'react';

export const BookEntry = ()  => {
  const [title, setTitle] = useState(''); //  Empty String
  const [outputURL1, setOutputURL1] = useState('');
  const [outputURL2, setOutputURL2] = useState('');
  const [outputURL3, setOutputURL3] = useState('');
  const [outputURL4, setOutputURL4] = useState('');
  const [outputURL5, setOutputURL5] = useState('');

  const [outputLink1, setOutputLink1] = useState('');
  const [outputLink2, setOutputLink2] = useState('');
  const [outputLink3, setOutputLink3] = useState('');
  const [outputLink4, setOutputLink4] = useState('');
  const [outputLink5, setOutputLink5] = useState('');

  var nameArr = [];

  return (
  <div id="form">
    <form>
        <input 
            style={{marginTop: "100px", marginLeft: "100px", width: "800px", border: "none",
            fontFamily: "Acme", fontSize: "25px", border: "none",borderBottom: "4px solid #581845"}}
            placeholder="Enter one of your favorite books"
            value={title}
        onChange={event => setTitle(event.target.value)}
        />
        <button 
            style={{color: "white",
            textTransform: 'uppercase', textDecoration: 'none', background: '#581845', padding: '10px', borderRadius: '5px',
            display: 'inline-block', border: 'none', transition: "all 0.4s ease 0s", fontFamily: "Acme", paddingRight: "35px", 
            paddingLeft: "35px", fontSize: "25px", margin: "10px"}} 
        onClick= {async () => {
          const book = {title};
          const response = await fetch("/input_book", {
            method: "POST",
            headers: {
              "Content_Type": "application/json"
            },
            body:
              JSON.stringify(book)
            })

          if (response.ok) {
            var form = document.getElementById("form") 
            // console.log("Response Worked! ");
            // console.log(JSON.stringify(response.url));
            // console.log(response);
            fetch("/novel_novel").then(response =>
              response.json().then(data => {
              nameArr = data.original_title.split(";")

              setOutputURL1(nameArr[0].substring(0,nameArr[0].indexOf(",")));
              setOutputURL2(nameArr[1].substring(0,nameArr[1].indexOf(",")));
              setOutputURL3(nameArr[2].substring(0,nameArr[2].indexOf(",")));
              setOutputURL4(nameArr[3].substring(0,nameArr[3].indexOf(",")));
              setOutputURL5(nameArr[4].substring(0,nameArr[4].indexOf(",")));
              // console.log(outputURL1);

              var url = "http://books.google.com/books?vid=ISBN"

              setOutputLink1(url.concat(nameArr[0].substring(nameArr[0].indexOf(",") + 1)))
              setOutputLink2(url.concat(nameArr[1].substring(nameArr[1].indexOf(",") + 1)))
              setOutputLink3(url.concat(nameArr[2].substring(nameArr[2].indexOf(",") + 1)))
              setOutputLink4(url.concat(nameArr[3].substring(nameArr[3].indexOf(",") + 1)))
              setOutputLink5(url.concat(nameArr[4].substring(nameArr[4].indexOf(",") + 1)))

              })
            ); 
          }
          else {
            console.log("Title not found")
            setTitle("We did not find this title. Please try again!")
          } 
        }
      }>
        Search</button>
    </form>
      <div style={{fontFamily: "Aclonica", fontSize:"20px", marginTop: "15px", marginLeft: "100px"}}>
        <p> {outputURL1} <a href={outputLink1}>{outputLink1}</a></p>
        <p> {outputURL2} <a href={outputLink2}>{outputLink2}</a></p>
        <p> {outputURL3} <a href={outputLink3}>{outputLink3}</a></p>
        <p> {outputURL4} <a href={outputLink4}>{outputLink4}</a></p>
        <p> {outputURL5} <a href={outputLink5}>{outputLink5}</a></p>
        <br/>
      </div>
  </div>
  );
};