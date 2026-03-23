import os
from flask import Flask, session, render_template
from .extensions import db
from .services.seed_service import seed_everything
from .services.auth_service import get_current_user
from .public.routes import public_bp
from .auth.routes import auth_bp
from .admin.routes import admin_bp
from .client.routes import client_bp
from .modules.financeiro.routes import financeiro_bp
from .modules.portfolio.routes import portfolio_bp


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///core_digital_aragao_r07.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-core-digital-aragao-r07'),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(financeiro_bp)
    app.register_blueprint(portfolio_bp)
    with app.app_context():
        db.create_all()
        seed_everything()

    @app.context_processor
    def inject_globals():
        return {
            'current_user': get_current_user(),
            'current_user_name': session.get('user_name'),
            'current_user_role': session.get('role'),
        }

    @app.errorhandler(404)
    def not_found(_error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(_error):
        return render_template('errors/500.html'), 500

    return app
