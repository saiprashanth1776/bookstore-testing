import React from "react"
import fire from "../Fire"
import { BrowserRouter as Router, Link, Route } from "react-router-dom"
import Recommendation from "./Recommendation"
import Books from "./Books"

var styleSection = {
	fontSize: "75px", 
	fontFamily: "Bangers",
	color: "#C70039"
}

var styleSection1 = { 
	fontSize: "25px", 
	fontFamily: "Acme",
}

class Header extends React.Component{

	constructor(props) {
        super(props);
        this.logout = this.logout.bind(this);
    }

    logout() {
        fire.auth().signOut();
    }

    // pathname = (e) => {
    // 	e.preventDefault();
    	
    // }

    render(){
		return(
			<Router>
					<nav className="navbar navbar-inverse">
					  <div className="container-fluid">
					    <div className="navbar-header">
					      <p className="navbar-brand" style={styleSection}>Boogle</p>
					    </div>
						    <ul style={styleSection1} className="nav navbar-nav navbar-right">
						      <li><Link onclick = {window.location.search = "", window.location.hash = "#hello"} 
						      	   style={{color: "#C70039"}} to="/recommendation">
						      	   <span className="glyphicon glyphicon-book"></span> 
						      	   Recommendations</Link>
						      </li>
						      <li><Link style={{color: "#C70039"}} to="/books">
						      	  <span className="glyphicon glyphicon-search"></span> 
						          Books</Link></li>
						      <li><a style={{color: "#C70039"}} href="hello" onClick={this.logout}>
						          <span className="glyphicon glyphicon-log-out"></span> 
						          Log Out</a></li>
						    </ul>
					  </div>
					</nav>
				<Route path="/recommendation" component={ Recommendation }/>
				<Route path="/books" component={ Books }/>
			</Router>
		)
	}
}

export default Header