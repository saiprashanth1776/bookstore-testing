import React from 'react'
import logo from './logo.svg'
import './App.css'
import Header from "./components/Header"
import Recommendation from "./components/Recommendation"
import fire from "./Fire"
import Rss from "./components/Rss"

class App extends React.Component {

	constructor() {
	    super();
	    this.state = ({
	      user: null,
	    });
	    this.authListener = this.authListener.bind(this);
	}

	componentDidMount() {
    this.authListener();
  	}

  	authListener() {
    	fire.auth().onAuthStateChanged((user) => {
      		console.log(user);
      		if (user) {
        		this.setState({ user });
      		} 
      		else {
        		this.setState({ user: null });
      		}
    	});
  	}	

  	render(){
	  	return (
	    	<div className="App">
	    		{this.state.user ? (
	    			<div>
	    				<Header />
	    			</div>
	    		) :
	    		(
	    			<div>
		    			<Rss />
		    		</div>
	    		)}
	    	</div>
	  	)
	}
}

export default App;
