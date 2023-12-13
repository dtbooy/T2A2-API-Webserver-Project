from app import db, bcrypt
from models.book import Book, BookSchema, CATEGORIES
from models.wanted_book import WantedBook, WantedBookSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required 
from flask import Blueprint, request, abort
from controllers.auth_controller import is_user_or_admin

wanted_books = Blueprint("wanted_books", __name__, url_prefix="<user_id>/wanted-books")

# GET ALL BOOKS IN WANTED BOOKS 
@wanted_books.route("/", methods=["GET"])
@jwt_required()
def get_wishlist(user_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # DB search for user with user_id
    stmt = db.select(User).where(User.id == user_id)
    user = db.session.scalar(stmt)
    return UserSchema(only=["wanted_books"]).dump(user), 201

# CREATE: ADD WANTED BOOK
@wanted_books.route("/", methods=["POST"])
@jwt_required()
def add_wanted_book(user_id):
    # Verify user credentials - only user can add books to owned books
    is_user_or_admin(user_id)
    # input data required = [book_id] optional data = [quality]
    # Load book data through schema
    book_info = WantedBookSchema(exclude=["id"]).load(request.json)
    # DB Search for book with book_id
    stmt = db.select(Book).where(Book.id == book_info["id"])
    book = db.session.scalar(stmt)
    # Return error if book not in database
    if not book:
         return {"error": "Book not found"}, 400
    # Add book to owned books register
    book_entry = WantedBook(
        book_id = book.id,
        user_id = user_id,
        quality = book.get("quality", "any")
    )
    db.session.add(book_entry)
    db.session.commit()

    return WantedBookSchema(["book", "quality"]).dump(book_entry), 201

# DELETE BOOK FROM USER WANTED BOOKS
@wanted_books.route("/<book_id>", methods=["DELETE"])
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

# RETURN BOOKS FROM <SECTION>
@wanted_books.route("/categories/<category>", methods=["GET"])
@jwt_required()
def get_wanted_book_category(user_id, category):
    # check valid category
    if not category in CATEGORIES:
        abort(400, f"Invalid category. Valid categories are: {CATEGORIES}")
    
    