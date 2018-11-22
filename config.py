import os

class Config(object):
    '''main config class'''
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

class DevelopmentConfig(Config):
    '''testing config for development'''
    DEBUG = True

class TestingConfig(Config):
    '''testing config for local before deployment'''
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    '''production configs'''
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'staging': Config,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
