import sys
import os

# เพิ่ม path ปัจจุบันให้ Python หาเจอ
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Menu, DailySale, Ingredient, Recipe

# สร้าง instance ของแอป
app = create_app()

# สร้างตารางฐานข้อมูล (เฉพาะตอน Deploy ครั้งแรก)
with app.app_context():
    db.create_all()
    print("✅ สร้างฐานข้อมูลเรียบร้อย!")

# ใช้สำหรับ Vercel Serverless
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))