import sys
import os

# เพิ่ม path ของโปรเจค
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Menu, DailySale, Ingredient, Recipe

app = create_app()

# สร้างฐานข้อมูล
with app.app_context():
    db.create_all()

# Vercel handler
def handler(request):
    return app(request)