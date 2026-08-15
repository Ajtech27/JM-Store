 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

 
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///markets.db'
    app.config['SECRET_KEY'] = '9f02f163fb48822d3cc8d603'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
     
    db.init_app(app)
    login_manager.init_app(app)
    app.app_context().push()
    bcrypt.init_app(app)
    # Import and register routes
    from market.route import register_routes
    register_routes(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        from market.model import User  # Import here to avoid circular import
        return User.query.get(int(user_id))
    login_manager.login_view = 'login_page'
    login_manager.login_message_category = 'info'
    return app
