from app import create_app, db
from app.models import Menu, DailySale, Ingredient, Recipe

app = create_app()

with app.app_context():
    db.drop_all()  # ⚠️ ลบตารางเก่า (เฉพาะตอนเปลี่ยนโมเดล)
    db.create_all()
    print("✅ สร้างฐานข้อมูลใหม่เรียบร้อย!")

if __name__ == '__main__':
    # ✅ แก้ให้คนอื่นใช้ได้
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False เพื่อความปลอดภัย