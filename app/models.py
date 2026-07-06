from app import db
from datetime import datetime

# ตารางวัตถุดิบ
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)  # ราคาทั้งชุด
    total_quantity = db.Column(db.Float, nullable=False)  # ปริมาณทั้งหมด (กรัม)
    unit = db.Column(db.String(20), default='กรัม')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    recipes = db.relationship('Recipe', backref='ingredient', lazy=True, cascade='all, delete-orphan')
    
    @property
    def cost_per_gram(self):
        """ต้นทุนต่อ 1 กรัม"""
        if self.total_quantity > 0:
            return self.total_cost / self.total_quantity
        return 0
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'

# ตารางสูตรอาหาร (เชื่อมวัตถุดิบกับเมนู)
class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    grams_per_dish = db.Column(db.Float, nullable=False)  # ✅ ใช้กี่กรัมต่อ 1 จาน
    
    def __repr__(self):
        return f'<Recipe menu={self.menu_id} ingredient={self.ingredient_id}>'

# ตารางเมนูอาหาร
class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)  # ราคาขายต่อจาน
    category = db.Column(db.String(20), nullable=False)  # 'delivery' หรือ 'instore'
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    recipes = db.relationship('Recipe', backref='menu', lazy=True, cascade='all, delete-orphan')
    sales = db.relationship('DailySale', backref='menu', lazy=True, cascade='all, delete-orphan')
    
    @property
    def cost_per_dish(self):
        """ต้นทุนต่อจาน (คำนวณจากวัตถุดิบ)"""
        total_cost = 0
        for recipe in self.recipes:
            ingredient = recipe.ingredient
            # ✅ คำนวณจากกรัมที่ใช้ต่อจาน
            if ingredient.total_quantity > 0:
                cost = ingredient.cost_per_gram * recipe.grams_per_dish
                total_cost += cost
        return total_cost
    
    @property
    def profit_per_dish(self):
        """กำไรต่อจาน"""
        return self.price - self.cost_per_dish
    
    def __repr__(self):
        return f'<Menu {self.name}>'

# ตารางยอดขาย
class DailySale(db.Model):
    __tablename__ = 'daily_sales'
    
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.Date, nullable=False, default=datetime.now().date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<DailySale menu_id={self.menu_id} date={self.sale_date}>'
    
    @property
    def revenue(self):
        """รายได้รวม = ราคาขาย × จำนวน"""
        return self.menu.price * self.quantity
    
    @property
    def total_cost(self):
        """ต้นทุนรวม = ต้นทุนต่อจาน × จำนวน"""
        return self.menu.cost_per_dish * self.quantity
    
    @property
    def profit(self):
        """กำไรสุทธิ = (ราคาขาย - ต้นทุน) × จำนวน"""
        return (self.menu.price - self.menu.cost_per_dish) * self.quantity