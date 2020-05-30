from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# import MySQLdb

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://whadmin:Password123#@wealthharvest.database.windows.net:1433/wealthharvest?driver=ODBC Driver 17 for SQL Server'

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
    from freedebtapp.blueprints.authorize import authorize as auth_blueprint
    app.register_blueprint(auth_blueprint.authorize)

    # blueprint for non-authorize parts of app
    from freedebtapp.blueprints.staticpages import static as static_blueprint
    app.register_blueprint(static_blueprint.main)

    from freedebtapp.blueprints.payments import payments as payments_blueprint
    app.register_blueprint(payments_blueprint.payment)

    from freedebtapp.blueprints.survey import survey as survey_blueprint
    app.register_blueprint(survey_blueprint.surveys)

    from freedebtapp.blueprints.investments import invest as invest_blueprint
    app.register_blueprint(invest_blueprint.investment)

    from freedebtapp.blueprints.wallet import wallet as wallet_blueprint
    app.register_blueprint(wallet_blueprint.wallets)

    from freedebtapp.blueprints.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint.profiles)

    from freedebtapp.blueprints.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint.dashboards)

    return app


