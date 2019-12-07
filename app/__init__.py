from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask import json
from redis import Redis
import rq



bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name = config):
    app = Flask(__name__, static_folder = 'templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('forum-tasks', connection = app.redis)

    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    from .sched import sched as sched_blueprint
    app.register_blueprint(sched_blueprint, url_prefix = '/sched')

    from .roomres import roomres as roomres_blueprint
    app.register_blueprint(roomres_blueprint, url_prefix = '/roomres')

    from .forum import forum as forum_blueprint
    app.register_blueprint(forum_blueprint, url_prefix = '/forum')

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix = '/profile')

    from .upload import upload as upload_blueprint
    app.register_blueprint(upload_blueprint, url_prefix = '/upload')

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix = '/profile')

    from .prescript import prescript as prescript_blueprint
    app.register_blueprint(prescript_blueprint, url_prefix = '/prescript')

    return app
