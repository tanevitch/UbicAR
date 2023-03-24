from os import environ


class Config(object):
    """Base configuration."""

    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"
    SECRET_KEY = "secret"

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class ProductionConfig(Config):
    """Production configuration."""
    DB_HOST = environ.get("DB_HOST", "DB_HOST")
    DB_USER = environ.get("DB_USER", "DB_USER")
    DB_PASS = environ.get("DB_PASS", "DB_PASS")
    DB_NAME = environ.get("DB_NAME", "DB_NAME")
    SQLALCHEMY_DATABASE_URI= (f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}")

class DevelopmentConfig(Config):
    """Development configuration."""

    DB_HOST = environ.get("DB_HOST", "MY_DB_HOST")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_DATABASE_URI= (f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}")

class TestingConfig(Config):
    """Testing configuration."""
    DB_HOST = environ.get("DB_HOST", "MY_DB_HOST")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_DATABASE_URI= (f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}")


config = dict(
    development=DevelopmentConfig, test=TestingConfig, production=ProductionConfig
)

## More information
# https://flask.palletsprojects.com/en/2.0.x/config/
