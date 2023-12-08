import os

class Config(object):
    # access to .env and get the value of SECRET_KEY, the variable name can be any but needs to match
    JWT_SECRET_KEY =  os.environ.get("SECRET_KEY")
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # access to .env and get the value of DATABASE_URL, the variable name can be any but needs to match
        value = os.environ.get("DB_URI")
        if not value:
            raise ValueError("DATABASE_URL is not set")
        return value

app_config = Config()