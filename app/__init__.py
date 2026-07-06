from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# สร้าง object สำหรับฐานข้อมูล
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # ตั้งค่า Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-12345')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/restaurant.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # เริ่มต้นใช้งานฐานข้อมูล
    db.init_app(app)
    migrate.init_app(app, db)
    
    # import routes
    from app.routes import menu_routes, sale_routes, report_routes, ingredient_routes
    
    # ลงทะเบียน routes
    app.register_blueprint(menu_routes.menu_bp)
    app.register_blueprint(sale_routes.sale_bp)
    app.register_blueprint(report_routes.report_bp)
    app.register_blueprint(ingredient_routes.ingredient_bp)
    
    return app