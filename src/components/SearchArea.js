import React from "react"

var input1 = {
  width: "500px",
  marginLeft: "250px",
  border: "none",
  borderBottom: "4px solid #581845",
  fontFamily: "Acme",
  fontSize: "30px"
}

var button1 = {
  color: "white",
  marginLeft: "10px",
  textTransform: 'uppercase',
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
  fontSize: "25px"
}

var select = {
  width: "120px",
  height: '57px',
  fontSize: "25px",
  fontFamily: "Acme",
  border: '1px solid #999',
  fontSize: '25px',
  color: 'white',
  backgroundColor: '#581845',
  borderRadius: "5px",
}

const SearchArea = (props) => {	
	return(
		<div className="search">
			<form style={{width: "1500px"}}>
				<input style={input1} onChange={props.searchHandle} type="text" />
				<button style={button1} type="submit" onClick={props.bookSearch}>Search</button>
				<select style={select} defaultValue="Sort" onChange={props.sortHandle}>
					<option disabled value="sort">Sort</option>
					<option value="Newest">New</option>
					<option value="Oldest">Old</option>
				</select>
			</form>
		</div>
	)
}

export default SearchArea
