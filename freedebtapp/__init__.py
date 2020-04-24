from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# import MySQLdb

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    # 'mysql://wealthadmin:freeDebt#357@wealtharvest/wealtharvestdb'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://wealthadmin:freeDebt#357@wealtharvest.database.windows.net:1433/wealtharvestdb'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://wealthadmin:freeDebt#357@wealtharvest.database.windows.net:1433/wealtharvestdb'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://wealthadmin:freeDebt#357@wealtharvest.database.windows.net:1433/wealtharvestdb?driver=SQL+Server+Native+Client+11.0'

    db.init_app(app)

    # For user session storage
    login_manager = LoginManager()
    login_manager.login_view = 'authorize.login'
    login_manager.init_app(app)

    from .models import User

    # Check if user is logged-in on every page load.
    @login_manager.user_loader
    def load_user(user_id):
        # User_email is unique
        if user_id is not None:
            ue = User.query.get(user_id)
            print(user_id)
            return ue
        return None

    # blueprint for authorize routes in our app
    from .authorize import authorize as auth_blueprint
    app.register_blueprint(auth_blueprint.authorize)

    # blueprint for non-authorize parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .survey import survey_blu as survey_blueprint
    app.register_blueprint(survey_blueprint)

    return app
