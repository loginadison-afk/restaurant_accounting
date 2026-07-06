import sys
import os

# ✅ เพิ่ม path สำหรับ Vercel
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Menu, DailySale, Ingredient, Recipe

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ สร้างฐานข้อมูลเรียบร้อย!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))