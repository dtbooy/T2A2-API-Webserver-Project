from controllers.users_controller import users
# from controllers.groups_contoller import groups
# from controllers.books_controller import books
from controllers.auth_controller import auth
from controllers.db_commands_controller import db_commands


registerable_controllers = [
    auth,
    users,
    # books,
    db_commands,
]