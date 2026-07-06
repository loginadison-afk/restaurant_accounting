from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dev-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/restaurant.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import menu_routes, sale_routes, report_routes, ingredient_routes
    
    app.register_blueprint(menu_routes.menu_bp)
    app.register_blueprint(sale_routes.sale_bp)
    app.register_blueprint(report_routes.report_bp)
    app.register_blueprint(ingredient_routes.ingredient_bp)
    
    return app