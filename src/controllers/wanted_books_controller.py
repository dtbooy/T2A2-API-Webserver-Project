from app import db, bcrypt
from models.book import Book, BookSchema, CATEGORIES
from models.wanted_book import WantedBook, WantedBookSchema
from models.user import User, UserSchema
from models.isbn import Isbn
from flask_jwt_extended import jwt_required 
from flask import Blueprint, request, abort
from controllers.auth_controller import is_user_or_admin

wanted_books = Blueprint("wanted_books", __name__, url_prefix="<int:user_id>/wanted-books")

# GET ALL BOOKS IN WANTED BOOKS 
@wanted_books.route("/", methods=["GET"])
@jwt_required()
def get_wishlist(user_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # DB search for user with user_id
    stmt = db.select(User).where(User.id == user_id)
    user = db.session.scalar(stmt)
    return UserSchema(only=["wanted_books"]).dump(user), 200

# CREATE: ADD WANTED BOOK
@wanted_books.route("/", methods=["POST", "PATCH", "PUT"])
@jwt_required()
def add_wanted_book(user_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # input data required = [book_id] optional data = [quality]
    # Load book data through schema
    book_info = WantedBookSchema(exclude=["id"]).load(request.json)
    # Check is wanted book entry exists 
    stmt = db.select(WantedBook).where(WantedBook.book_id == book_info["book_id"], WantedBook.user_id == user_id)
    exists = db.session.scalar(stmt)
    if exists:
        exists.quality = book_info.get("quality", "any")
        db.session.commit()
        return WantedBookSchema(only=["book", "quality"]).dump(exists), 200
    else:
        # DB Search for book with book_id
        stmt = db.select(Book).where(Book.id == book_info["book_id"])
        book = db.session.scalar(stmt)
        # Return error if book not in database
        if not book:
            return {"error": "Book not found"}, 400
        # Add book to owned books register
        book_entry = WantedBook(
            book_id = book.id,
            user_id = user_id,
            quality = book_info.get("quality", "any")
        )
        db.session.add(book_entry)
        db.session.commit()

        return WantedBookSchema(only=["book", "quality"]).dump(book_entry), 201

# DELETE BOOK FROM USER WANTED BOOKS
@wanted_books.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
def remove_wanted_book(user_id, book_id):
    # Verify user credentials - only user can add books to wanted books
    is_user_or_admin(user_id)
    # DB Search for book entry in UserBook with book_id & user_id
    stmt = db.select(WantedBook).where(WantedBook.book_id == book_id, WantedBook.user_id == user_id)
    book_entry = db.session.scalar(stmt)
    # Return error if book not in database
    if not book_entry:
        abort(404, "Book not in users owned-books")
    db.session.delete(book_entry)
    db.session.commit()
    return {}, 204

# RETURN BOOKS FROM <SECTION>
@wanted_books.route("/categories/<string:category>", methods=["GET"])
@jwt_required()
def get_wanted_book_category(user_id, category):
    # check valid category
    if not category in CATEGORIES:
        abort(400, f"Invalid category. Valid categories are: {CATEGORIES}")
    # Select all books where 
    stmt = db.select(WantedBook).join(Book).where(Book.category == category, WantedBook.user_id == user_id)
    books = db.session.scalars(stmt)
    return WantedBookSchema(many=True, only=["book", "quality"]).dump(books)

# RETURN WANTED BOOK FROM ISBN 
@wanted_books.route("/isbn/<string:isbn>", methods=["GET"])
@jwt_required()
def get_wanted_book_isbn(user_id, isbn):
    # check valid isbn
    stmt = db.select(Isbn).where(Isbn.isbn == isbn)
    check_isbn = db.session.scalar(stmt)
    if not check_isbn:
        return {"error" : "ISBN not in database"}, 404
    # Select row from wanted_books where WantedBook.user_id = <user_id> AND WantedBook.book_id = Book.id = Isbn.book_id where Isbn.isbn = <isbn>
    stmt = db.select(WantedBook).where(WantedBook.user_id == user_id).join(Book).join(Isbn).where(Isbn.isbn == isbn)
    book = db.session.scalar(stmt)

    return WantedBookSchema(only=["book","quality"]).dump(book)

