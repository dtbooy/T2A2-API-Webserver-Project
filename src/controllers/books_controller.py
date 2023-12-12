from app import db, bcrypt
from models.book import Book, BookSchema
from models.book_author import BookAuthor, BookAuthorSchema
from models.isbn import Isbn, IsbnSchema
from flask_jwt_extended import jwt_required 
from flask import Blueprint, request, abort
from controllers.auth_controller import is_admin

books = Blueprint("books", __name__, url_prefix="/books")

# CREATE: BOOKS
@books.route("/", methods=["POST"])
@jwt_required()
def create_book():
    # Book data required = [Title, ISBN(at least 1), author_ids, category, ]
    # Optional Book data = [series]
    # Extract other table columns
    isbn_info, author_ids = [request.json.pop("isbns"), request.json.pop("author_ids", None)]

    # check if book exists
    stmt = db.select(Isbn).where(Isbn.isbn.in_(isbn_info))
    isbn_exists = db.session.scalars(stmt).first()
    if isbn_exists:
         return {"error": "Book exists with provided ISBN", "Book details" : IsbnSchema().dump(isbn_exists)}, 400

    # Add data to book table
    book_info = BookSchema(exclude=["id"]).load(request.json)
    new_book = Book()
    new_book.title = book_info["title"]
    new_book.category = book_info["category"]
    new_book.series = book_info.get("series", None)
    db.session.add(new_book)
    db.session.commit()

    # Add book & author ids to book_author table 
    authors =[]
    for a in author_ids:
        authors.append(
            BookAuthor(
                book_id = new_book.id,
                author_id = int(a)
            )
        )
    db.session.add_all(authors)

    # Add ISBNs to ISBN table
    book_isbns = []
    for i in isbn_info:
        book_isbns.append(
            Isbn(
                isbn = i,
                book_id = new_book.id
        ))
    db.session.add_all(book_isbns)
    db.session.commit()

    return BookSchema().dump(new_book), 201

# READ: ALL BOOKS
@books.route("/", methods=["GET"])
@jwt_required()
def get_books():
    # Only administrators can access Book list
    is_admin()
    # Database query: return all books
    stmt = db.select(Book)
    print(stmt)
    books = db.session.scalars(stmt)
    return BookSchema(many=True).dump(books), 200

# READ: SINGLE BOOK
@books.route("/<int:book_id>", methods=["GET"])
@jwt_required()
def get_book(book_id):
    # Database query: return book with book_id
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    # Check book exists
    if not book:
        return {"Error": "Book not found"}, 404
    return BookSchema().dump(book), 200

# UPDATE: Book
@books.route("/<int:book_id>", methods=["PATCH"])
@jwt_required()
def update_books(book_id):
    # Only administrator can edit book details
    is_admin()
    # Database query: return book with book_id
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    # Check book exists
    if not book:
        return {"Error": "Book not found"}, 404
    
    # Extract related table data from request
    isbn_info, author_ids = [request.json.pop("isbns", None), request.json.pop("author_ids", None)]    
    # validate updated book info through schema 
    book_info = BookSchema(exclude=["id"]).load(request.json)
    # Update book elements
    book.title = book_info.get("title", book.title)
    book.category = book_info.get("category", book.category)
    book.series = book_info.get("series", book.series)
    db.session.commit()

    # Update ISBNs if provided
    if isbn_info:
        # Remove previous Isbns from ISBN table
        stmt = db.select(Isbn).filter_by(book_id=book.id)
        isbns = db.session.scalars(stmt).all()
        for i in isbns:
            db.session.delete(i)
        db.session.commit()
        # Add new ISBNs to ISBN table
        book_isbns = []
        for i in isbn_info:
            book_isbns.append(
                Isbn(
                    isbn = i,
                    book_id = book.id
            ))
        db.session.add_all(book_isbns)
        db.session.commit()

    # Update Book_Authors if provided
    if author_ids:
        rm_stmt = db.select(BookAuthor).filter_by(book_id=book.id)
        rm_works = db.session.scalars(rm_stmt).all()
        for work in rm_works:
            db.session.delete(work)
        db.session.commit()
        # Add book & author ids to book_author table 
        authors =[]
        for a in author_ids:
            authors.append(
                BookAuthor(
                    book_id = book.id,
                    author_id = int(a)
                )
            )
        db.session.add_all(authors)
        db.session.commit()
    return BookSchema().dump(book), 200
    
# DELETE: BOOK
@books.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    # Only administrator can delete book
    is_admin()
    # Database query: return book with id <book_id>
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    # Ensure book exists
    if not book:
        return {"Error": "Book not found"}, 404
    # delete book from database & commit
    db.session.delete(book)
    db.session.commit()
    # return empty body & 204 No Content response
    return {}, 204