from flask import Blueprint
from app import db, bcrypt

# Import all models for Create Tables command
from models.author import Author, AuthorSchema
from models.isbn import Isbn, IsbnSchema
from models.user_book import UserBook, UserBookSchema
from models.user_group import UserGroup, UserGroupSchema
from models.user_wishlist import UserWishlist, UserWishlistSchema
from models.user import User, UserSchema
from models.book import Book, BookSchema
from models.book_author import BookAuthor, BookAuthorSchema 
from models.group import Group, GroupSchema

db_commands = Blueprint("db", __name__)

# CLI COMMANDS AREA
@db_commands.cli.command("drop")
def drop():
    db.drop_all()
    print("Tables Dropped")

@db_commands.cli.command("create")
def create():
    db.drop_all()
    print("Tables Dropped")
    db.create_all()
    print("Tables Created")

@db_commands.cli.command("seed")
def seed():
    pass
    #1 Seed Users
    users = [
        User(
            username = "JamesHolden",
            password = bcrypt.generate_password_hash("ISawAButtonAndPressedIt").decode("utf-8")
        ),
        User(
            username = "NaomiNagata",
            password = bcrypt.generate_password_hash("FilipInaros").decode("utf-8")
        ),
        User(
            username = "AlexKamal",
            password = bcrypt.generate_password_hash("DONKEYBALLS3").decode("utf-8")
        ),
        User(
            username = "AmosBurton",
            password = bcrypt.generate_password_hash("You could be both").decode("utf-8")
        ),
        User(
            username = "JasonAsano",
            password = bcrypt.generate_password_hash("ImGoodAtPeople").decode("utf-8")
        ),
        User(
            username = "FarraHurin",
            password = bcrypt.generate_password_hash("LavaCannons").decode("utf-8")
        ),
        User(
            username = "GarethZandier",
            password = bcrypt.generate_password_hash("AreWeTheBloodCultNow?").decode("utf-8")
        ),
        User(
            username = "Test_Administrator",
            password = bcrypt.generate_password_hash("Admin123").decode("utf-8"),
            is_admin = True
        )
    ]
    db.session.add_all(users)

    #2 Seed Groups
    # HWFWM open group - no password required to join
    # Rocinante - password protected group
    groups = [
        Group(
            name = "rocinante",
            password = bcrypt.generate_password_hash("NoLongerAWorkHorse").decode("utf-8")
        ),
        Group(
            name = "HWFWM"
        )
    ]
    db.session.add_all(groups)
    db.session.commit()

    #3 Seed User_groups (Join table)
    # Expanse characters in the Rocinante group
    # HWFWM Character in the HWFWM group
    # James Holden in both groups
    # Admin has no groups, but access to everything

    user_groups = [
        UserGroup(
            user_id = users[0].id,
            group_id= groups[0].id
        ),
        UserGroup(
            user_id = users[1].id,
            group_id= groups[0].id
        ),
        UserGroup(
            user_id = users[2].id,
            group_id= groups[0].id
        ),
        UserGroup(
            user_id = users[3].id,
            group_id= groups[0].id
        ),
        UserGroup(
            user_id = users[4].id,
            group_id= groups[1].id
        ),
        UserGroup(
            user_id = users[5].id,
            group_id= groups[1].id
        ),
        UserGroup(
            user_id = users[6].id,
            group_id= groups[1].id
        ),
        UserGroup(
            user_id = users[0].id,
            group_id= groups[1].id
        ),
    ]
    db.session.add_all(user_groups)
    db.session.commit()
    #4 Seed authors
    authors = [
        Author(
            surname = "Martin",
            given_names = "George R.R."
        ),
        Author(
            surname = "Tolken",
            given_names = "J.R.R."
        ),
        Author(
            surname = "Dick",
            given_names = "Phillip K."
        ),
        Author(
            surname = "Farmer",
            given_names = "Philip Jose Farmer"
        ),
        Author(
            surname = "Pratchett",
            given_names = "Terry"
        ),
        Author(
            surname = "Shirtaloon"
        ),
        Author(
            surname = "Deverell",
            given_names = "Travis"
        ),
        Author(
            surname = "Hobb",
            given_names = "Robin"
        ),
        Author(
            surname = "Gaiman",
            given_names = "Neil"
        )
    ]
    db.session.add_all(authors)
    db.session.commit()

    #6 Seed books 
    books = [
        Book(title ="Game of Thrones", category ="Science Fiction & Fantasy", series ="A song of ice and fire"), #0
        Book(title="A Clash of Kings", category="Science Fiction & Fantasy", series="A Song of Ice and Fire"),  #1
        Book(title="A Storm of Swords", category="Science Fiction & Fantasy", series="A Song of Ice and Fire"), #2
        Book(title="A Feast for Crows", category="Science Fiction & Fantasy", series="A Song of Ice and Fire"), #3
        Book(title="A Dance with Dragons", category="Science Fiction & Fantasy", series="A Song of Ice and Fire"), #4
        Book(title="The Fellowship of the Ring", category="Science Fiction & Fantasy", series="Lord of the Rings"), #5
        Book(title="The Two Towers", category="Science Fiction & Fantasy", series="Lord of the Rings"), #6
        Book(title="The Return of the King", category="Science Fiction & Fantasy", series="Lord of the Rings"), #7
        Book(title="Do Androids Dream of Electric Sheep", category="Science Fiction & Fantasy"), #8 
        Book(title="A Scanner Darkly", category="Science Fiction & Fantasy"), #9
        Book(title="The Maker of Universes", category="Science Fiction & Fantasy", series="World of Tiers"), #10
        Book(title="The Gates of Creation", category="Science Fiction & Fantasy", series="World of Tiers"), # 11
        Book(title="A Private Cosmos", category="Science Fiction & Fantasy", series="World of Tiers"), #12
        Book(title="Behind the Walls of Terra", category="Science Fiction & Fantasy", series="World of Tiers"), #13
        Book(title="The Lavalite World", category="Science Fiction & Fantasy", series="World of Tiers"), #14
        Book(title="Red Orc's Rage", category="Science Fiction & Fantasy", series="World of Tiers"), #15
        Book(title="More Than Fire", category="Science Fiction & Fantasy", series="World of Tiers"), #16
        Book(title="He Who Fights With Monsters", category="Science Fiction & Fantasy", series="He Who Fights With Monsters"), #17
        #     category="Science Fiction & Fantasy", 
        #     series=" "),
        # Book(
        #     title=" ", 
        #     category="Science Fiction & Fantasy", 
        #     series=" "),
        # Book(
        #     title=" ", 
        #     category="Science Fiction & Fantasy", 
        #     series=" "),
        # Book(
        #     title=" ", 
        #     category="Science Fiction & Fantasy", 
        #     series=" "),
        # Book(
        #     title=" ", 
        #     category="Science Fiction & Fantasy", 
        #     series=" "),
        # Book(
        #     title=" ", 
        #     category="Science Fiction & Fantasy", 
        #     series=" "),
    ]

    db.session.add_all(books)
    db.session.commit()
     

    #6 Seed ISBNs
    isbn_dict = {
        0 : ["9780553381689", "9780553386790", "9780553573404", "9780553593716"], 
        1 : ["9781984821157", "9780006479895", "9780307987648", "9780002245852", "9781984821164", "9780008363741", "9781892065322", "9780553579901", "9780553381696", "9780553108033", "9780345535412"],
        2 : ["9780007447848", "9781783207848", "9780007447855", "9780593158968", "9780008412760", "9781892065841", "9780553573428", "9780553381702", "9780593158951", "9780007456352", "9780345543981"],
        3 : ["9780553582024", "9780553390575", "9780553582031", "9780553801507", "9780553390568", "9780606267267"],
        4 : ["9780553582017", "9780553385953", "9780553905656", "9780553841121", "9781101886038", "9781101886045"],
        5 : ["9780618260515", "9780007136599", "9780358380238", "9780618153985"],
        6 : ["9780395647400", "9780007136568", "9780007203550"],
        7 : ["9780606013024", "9780261103597", "9780007129720"],
        8 : ["9781615233595", "1615233598", "9781608866403", "9780194230636", "9780345404473", "9780575079939"],
        9 : ["9780547572178", "9781400096909", "9780679736653"],
        10 : ["9780722134535", "9780441516216"],
        11 : ["9780722134436"],
        12 : ["9780441077243"],
        13 : ["9780932096135", "9780722134450"],
        14 : ["9780932096210", "9780441474202"],
        15 : ["9780312850364", "9780812508901"],
        16 : ["9780575119659", "9780312852801", "0312852800"],
        17 : ["9798712811786", "9789798712814"],
        18 : [],
        19 : [],
        20 : [],
        21 : [],
        22 : [],
        23 : [],
        24 : [],
        25 : [],
        26 : [],
        27 : [],
        28 : [],
        29 : [],
    }
    isbns = []
    for k, v in isbn_dict.items():
        for value in v:
            isbns.append(
                Isbn(
                    isbn = int(value),
                    book_id = books[k].id
            ))

    db.session.add_all(isbns)
    db.session.commit()


    #7 Seed book_author (book_authors join table)
    book_authors_dict = {0 : [0,1,2,3,4], 1 : [5,6,7], 2 : [8,9,7], 3 : [10,11,12,13,14,15,16], 5: [17], 6 : [17]}
    book_authors = []
    for k, v in book_authors_dict.items():
        for value in v:
            book_authors.append(BookAuthor(author_id = authors[k].id, book_id = books[value].id ))
   
    db.session.add_all(book_authors)
    db.session.commit()
    #8 Seed users_books (join Table - Bookshelf)
    bookshelf_dict = {0 : [0,1,3,4,7,9,12], 1 : [0,5,6,7,16], 2 : [], 3 : [10,11,12,13,14,15,16], 4 :[12,5,3,6,7], 5: [11], 6 : [1], 7:[0]}
    bookshelf = []
    for k, v in bookshelf_dict.items():
        for value in v:
            bookshelf.append(UserBook(user_id = users[k].id, book_id = books[value].id ))
   
    db.session.add_all(bookshelf)
    db.session.commit()

    # #9 Seed users_wishlist (join table - Wish list)
    wishlists_dict = {0 : [2, 5, 6, 8], 1 : [10,11,12,13,14,15], 2 : [0,1,2,3,4], 3 : [5,6,7], 4 :[0,1,2,4], 5: [10,12,13], 6 : [0,2,3,4], 7:[1,2]}
    users_wishlists = []
    for k, v in wishlists_dict.items():
        for value in v:
            users_wishlists.append(UserWishlist(user_id = users[k].id, book_id = books[value].id))
   
    db.session.add_all(users_wishlists)
    db.session.commit()
    print("Tables Seeded")