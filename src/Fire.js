import firebase from 'firebase';

const config = {
  apiKey: "AIzaSyDUr3WGT3p3hBiaDETsrrUG9jtr_yTL6KY",
  authDomain: "bookstore-cce6f.firebaseapp.com",
  databaseURL: "https://bookstore-cce6f.firebaseio.com",
  projectId: "bookstore-cce6f",
  storageBucket: "bookstore-cce6f.appspot.com",
  messagingSenderId: "989175389164"
};
const fire = firebase.initializeApp(config);
export default fire;