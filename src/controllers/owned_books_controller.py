from app import db, bcrypt
from models.book import Book, BookSchema
from models.user_book import UserBook, UserBookSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required 
from flask import Blueprint, request, abort
from controllers.auth_controller import is_user_or_admin

owned_books = Blueprint("owned_books", __name__, url_prefix="<user_id>/owned-books")

# GET ALL BOOKS IN BOOKSHELF (UserBooks)
@owned_books.route("/", methods=["GET"])
@jwt_required()
def get_bookshelf(user_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # DB search for user with user_id
    stmt = db.select(User).where(User.id == user_id)
    user = db.session.scalar(stmt)
    # Return error if user not in database
    if not user:
        return {"error": "User not found"}, 400
    return UserSchema(only=["books"]).dump(user), 201

# CREATE: ADD BOOK
@owned_books.route("/", methods=["POST"])
@jwt_required()
def add_book(user_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # input data required = [book_id]
    # Load book data through schema
    book_info = UserBookSchema(exclude=["id"]).load(request.json)
    # DB Search for book with book_id
    stmt = db.select(Book).where(Book.id == book_info["id"])
    book = db.session.scalar(stmt)
    # Return error if book not in database
    if not book:
         return {"error": "Book not found"}, 400
    # Add book to owned books register
    book_entry = UserBook(
        book_id = book.id,
        user_id = user_id
    )
    db.session.add(book_entry)
    db.session.commit()

    return UserBookSchema(only="book").dump(book_entry), 201

# DELETE BOOK FROM USER OWNED BOOKS
@owned_books.route("/<book_id>", methods=["DELETE"])
@jwt_required()
def remove_book(user_id, book_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # DB Search for book entryin UserBook with book_id & user_id
    stmt = db.select(UserBook).where(UserBook.book_id == book_id, UserBook.user_id == user_id)
    book_entry = db.session.scalar(stmt)
    # Return error if book not in database
    if not book_entry:
         return {"error": "Book not in users owned-books"}, 404
    db.session.delete(book_entry)
    db.session.commit()