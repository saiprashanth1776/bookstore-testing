import React from "react"
import BookCard from "./BookCard"

const ListBooks = (props) => {
	return(
		<div style={{display: "grid", margin: "20px 0 50px 0",
    gridTemplateColumns: 'repeat(4, 1fr)', gridAutoRows: '1fr', gridGap: '1em'}}>
		{
			props.books.map((book, index) => {

				return <BookCard 
					key = {index}
					image = {book.volumeInfo.imageLinks.thumbnail}
					title = {book.volumeInfo.title}
					authors = {book.volumeInfo.authors}
					publish = {book.volumeInfo.publishedDate.substring(0,4)}
					link = {book.volumeInfo.infoLink}
				/>
			})
		}
		</div>
	)
}

export default ListBooks