# blog ---> __init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.template_filter('nl2br')
def nl2br_filter(text):
        return text.replace('\n', '<br>')

################################
# Setup Database ###############
################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///'+os.path.join(basedir, 'data.sqlite')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

################################
# Login manager Configurations ##
################################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

################################
# Blueprint Configurations #####
################################

from blog.core.views import core  # noqa: E402
from blog.error_pages.handlers import error_pages  # noqa: E402
from blog.users.views import users  # noqa: E402
from blog.blog_posts.views import blog_posts # noqa: E402

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)

