from app import db, bcrypt
from models.book import Book, BookSchema
from models.user_book import UserBook, UserBookSchema
from models.user import User, UserSchema
from models.isbn import Isbn
from flask_jwt_extended import jwt_required 
from flask import Blueprint, request, abort
from controllers.auth_controller import is_user_or_admin

owned_books = Blueprint("owned_books", __name__, url_prefix="<int:user_id>/owned-books")

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
        return {"error": "User not found"}, 404
    return UserSchema(only=["owned_books"]).dump(user), 200

# CREATE: ADD BOOK
@owned_books.route("/", methods=["POST"])
@jwt_required()
def add_book(user_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # input data required = [book_id]
    # Load book data through schema
    book_info = UserBookSchema(exclude=["id"]).load(request.json)
    # Check book isn't already on bookshelf
    # return UserBook record where user is user_id and book is the submitted book_id
    stmt = db.select(UserBook).where(UserBook.book_id == book_info["book_id"], UserBook.user_id == user_id)
    check = db.session.scalar(stmt)
    if check:
        return {"error": "book already in owned_books"}, 400
    # DB Search for book with book_id
    stmt = db.select(Book).where(Book.id == book_info["book_id"])
    book = db.session.scalar(stmt)
    # Return error if book not in database
    if not book:
         return {"error": "Book not found"}, 404
    # Add book to owned books register
    book_entry = UserBook(
        book_id = book.id,
        user_id = user_id
    )
    db.session.add(book_entry)
    db.session.commit()

    return UserBookSchema(only=["book"]).dump(book_entry), 201

# DELETE BOOK FROM USER OWNED BOOKS
@owned_books.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
def remove_book(user_id, book_id):
    # Verify user credentials - only user can remove books from owned books
    is_user_or_admin(user_id)
    # DB Search for book entry in UserBook with book_id & user_id
    stmt = db.select(UserBook).where(UserBook.book_id == book_id, UserBook.user_id == user_id)
    book_entry = db.session.scalar(stmt)
    # Return error if book not in database
    if not book_entry:
         return {"error": "Book - User entry not found"}, 404
    db.session.delete(book_entry)
    db.session.commit()
    return {}, 204

# RETURN OWNED BOOK FROM ISBN 
@owned_books.route("/isbn/<string:isbn>", methods=["GET"])
@jwt_required()
def get_wanted_book_isbn(user_id, isbn):
    # Verify user credentials - only user can search owned books 
    is_user_or_admin(user_id)
    # check valid isbn - return isbn record for isbn
    stmt = db.select(Isbn).where(Isbn.isbn == isbn)
    check_isbn = db.session.scalar(stmt)
    if not check_isbn:
        return {"error" : "ISBN not in database"}, 404

    # Select row from user_books where UserBook.user_id = <user_id> AND UserBook.book_id = Book.id = Isbn.book_id where Isbn.isbn = <isbn>
    stmt = db.select(UserBook).where(UserBook.user_id == user_id).join(Book).join(Isbn).where(Isbn.isbn == isbn)
    book = db.session.scalar(stmt)
    # Returns book details if in Users bookshelf, or empty blank if not 
    return UserBookSchema(only=["book"]).dump(book)
