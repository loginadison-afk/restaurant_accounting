from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# สร้าง object สำหรับฐานข้อมูล
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # เริ่มต้นใช้งานฐานข้อมูล
    db.init_app(app)
    migrate.init_app(app, db)
    
    # import routes (เพิ่ม ingredient_routes)
    from app.routes import menu_routes, sale_routes, report_routes, ingredient_routes
    
    # ลงทะเบียน routes (เพิ่ม ingredient_bp)
    app.register_blueprint(menu_routes.menu_bp)
    app.register_blueprint(sale_routes.sale_bp)
    app.register_blueprint(report_routes.report_bp)
    app.register_blueprint(ingredient_routes.ingredient_bp)  # ✅ เพิ่มบรรทัดนี้
    
    return app