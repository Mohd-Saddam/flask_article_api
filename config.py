# class Config:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///article.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# Base configuration class with shared configurations.
# Config class containing common configuration options
class Config:
    """
    Base configuration class with shared configurations.
    """
    # Disable SQLAlchemy modification tracking to suppress a warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disables modification tracking for SQLAlchemy to suppress a warning about significant overhead.

# DevelopmentConfig inherits from Config, setting up the SQLite database for development
class DevelopmentConfig(Config):
    """
    Configuration class for development environment.

    Inherits from Config and sets up the SQLite database for development.
    """

    # SQLite database URI for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///article.db'

# TestingConfig inherits from Config, setting up the SQLite database for testing
class TestingConfig(Config):
    """
    Configuration class for testing environment.

    Inherits from Config and sets up the SQLite database for testing.
    """

    # SQLite database URI for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing_use.db'

    # Set TESTING to True for testing environment
    TESTING = True  #Sets the TESTING flag to True for the testing environment. This flag is often used to customize behavior when running tests.

