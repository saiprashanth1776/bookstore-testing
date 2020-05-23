import React from "react"

var sectionStyle = {
  backgroundColor: "#581845",
  color: "white",
  fontSize: "15px",
  fontFamily: "Aclonica",
  textDecoration: "none",
  textTransform: 'uppercase',
}

var link = {
  color: "white",
  textDecoration: 'none',
  background: '#581845',
  padding: '10px',
  borderRadius: '5px',
  display: 'inline-block',
  border: 'none',
  transition: "all 0.4s ease 0s",
  fontFamily: "Acme",
  paddingRight: "35px", 
  paddingLeft: "35px",
  fontSize: "20px"
}

const BookCard = (props) => {
	return(
		<div style={{border: "4px solid #581845", color: "#581845", borderRadius: "5px"}}>
			<img src={props.image} alt="" />
			<div style={{ height: '240px', padding: '10px'}}>
				<h3>{props.title}</h3>
				<h4>Authors: {props.authors}</h4>
        <h5>Published: {props.publish}</h5>
				<a style = { link } href={props.link}>View Here</a>
			</div>
		</div>
	)
}

export default BookCard