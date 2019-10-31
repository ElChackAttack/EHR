import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Config base class contains settings common to all configurations
#Different subclasses define settings specific to a configuration
class Config:
    SECRET_KEY = os.environ.get('EHR_KEY') or 'password'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('EHR_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') #os.environ.get('MAIL_PASSWORD')
    SYSTEM_MAIL_SUBJECT_PREFIX = '[HealthHub]'
    SYSTEM_MAIL_SENDER = 'healthhubnotify@gmail.com'
    SYSTEM_ADMIN = os.environ.get('SYSTEM_ADMIN')

    #method takes application insatnce as argument
    #allows config-specific initialization to be performed
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
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
