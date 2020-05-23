import React from "react"
import Popup from "reactjs-popup"
import fire from '../Fire';

var sectionStyle = {
	fontFamily: "Handlee",
    color: "#4A1137",
    fontSize: "25px",
}

var button1 = {
  color: "white",
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
  fontSize: "30px",
  marginLeft: "600px"
}

var button2 = {
  color: "white",
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
  fontSize: "30px",
}

var input1 = {
  marginTop: "10px",
  width: "700px",
  border: "none",
  borderBottom: "4px solid #581845",
  fontFamily: "Acme",
  fontSize: "30px"
}

var input2 = {
  marginTop: "5px",
  width: "700px",
  border: "none",
  borderBottom: "4px solid #581845",
  fontFamily: "Acme",
  fontSize: "30px"
}

class Rss extends React.Component{
	constructor(){
		super();
		this.state = {
      email: '',
      password: '',
			recentInfo: {
				name: '',
				url: '',
				description: ''
			}
		}
		this.login = this.login.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.signup = this.signup.bind(this);
	}

	handleChange(e) {
		// console.log(this.state.email)
	    this.setState({ [e.target.name]: e.target.value });
	};

	login(e) {
  	e.preventDefault();
  	fire.auth().signInWithEmailAndPassword(this.state.email, this.state.password).then((u)=>{
  	}).catch((error) => {
  		alert('Password is incorrect!')
      	console.log(error);
    	});
	};

	signup(e) {
  	e.preventDefault();
  	fire.auth().createUserWithEmailAndPassword(this.state.email, this.state.password).then((u)=>{
  	}).then((u)=>{console.log(u)})
  	.catch((error) => {
  		alert("Email address already existing!")
      	console.log(error);
    	})
	};

	RssFetchData(){
		var request = new XMLHttpRequest()
		var feed = document.getElementById("feed")
		feed.innerHTML = ""
		request.onreadystatechange = () => {
			if(request.readyState == 4 && request.status == 200){
				var root = request.responseXML.documentElement;
				for (var i = 0; i < 10; i++) {

                var items = root.getElementsByTagName("item")[i];

                console.log(items)

            		this.state.recentInfo.name = items.getElementsByTagName("title")[0].firstChild.nodeValue
            		this.state.recentInfo.url = items.getElementsByTagName("link")[0].firstChild.nodeValue
            		this.state.recentInfo.description = items.getElementsByTagName("description")[0].firstChild.nodeValue

          			var anchor = document.createElement("a")
          			anchor.align = "center"
          			anchor.innerHTML = this.state.recentInfo.name
          			anchor.class = "a"
          			anchor.href = this.state.recentInfo.url
          			var br = document.createElement("br")

          			var desc = document.createElement("p")
  	      			var desc1 = this.state.recentInfo.description
  	      			var desc2 = desc1.substring(desc1.indexOf("<p>"), desc1.length)
  	      			desc.innerHTML = desc2;

          			feed.appendChild(br)
          			feed.appendChild(anchor)
          			feed.appendChild(desc)
				}
			}
		}
		request.open("GET", "https://cors-anywhere.herokuapp.com/https://blog.bookstellyouwhy.com/rss.xml", true);
    request.send();
	}

	componentDidMount() {
    	{this.RssFetchData()}

  	}

	render(){
		return (
				<div style = { sectionStyle }>
					<br/>
					<h1 style={{marginLeft:"630px"}}> NEWS 
						<Popup trigger = 
						{
							<button style = {button1} position="center">Login</button>
						}
						modal
						closeOnDocumentClick>
						{close => (
							<div>
						        <form>
						          <div>
						            <input style={input1} onChange={this.handleChange} value={this.state.email} type="email" name="email" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
						          </div>
						          <div className="form-group">
						            <input style={input2} onChange={this.handleChange} value={this.state.password} type="password" name="password" id="exampleInputPassword1" placeholder="Password" />
						          </div>
						          <div style={{  marginLeft: "175px"}}>
						            <button style={button2} type="submit" onClick={this.login}>Login</button>
						            <button style={button2} onClick={this.signup}>Signup</button>
						          </div>
						        </form>
						    </div>
							)}
						</Popup>
					</h1>
          <div id="feed"></div>
				</div>
		)
	}
}

export default Rss