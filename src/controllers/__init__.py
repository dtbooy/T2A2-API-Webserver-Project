from controllers.users_controller import users
from controllers.groups_controller import groups
from controllers.books_controller import books
from controllers.auth_controller import auth
from controllers.db_commands_controller import db_commands


registerable_controllers = [
    auth,
    users,
    books,
    groups,
    db_commands,
]