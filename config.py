

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Config base class contains settings common to all configurations
#Different subclasses define settings specific to a configuration
class Config:
    SECRET_KEY = os.environ.get('EHR_KEY')
    SQALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = ''
    FLASKY_ADMIN = os.environ.get('EHR_ADMIN')

    #method takes application insatnce as argument
    #allows config-specific initialization to be performed
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = ''
    MAIL_PORT = 587 #Default
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EHR_MAIL_USER')
    MAIL_PASSWORD = os.environ.get('EHR_MAIL_PASS')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    #Development Config is registered as default
    'default' : DevelopmentConfig
}
