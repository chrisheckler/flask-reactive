
import os


class Config(object):
    """ Parent configuratioin class
    """
    DEBUG = True
    CSRF_ENABLED  = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """ Configuration for Development
    """
    DEBUG = True


class TestingConfig(Config):
    """ Configuration for Testing, with a seperate
        test database
    """ 
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """ Configuration for Staging
    """
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    """ Configuration for Production
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}


