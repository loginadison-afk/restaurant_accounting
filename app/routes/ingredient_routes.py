from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Ingredient, Recipe, Menu

ingredient_bp = Blueprint('ingredient', __name__, url_prefix='/ingredient')

# แสดงรายการวัตถุดิบ
@ingredient_bp.route('/')
def list_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('ingredient/list.html', ingredients=ingredients)

# เพิ่มวัตถุดิบ
@ingredient_bp.route('/add', methods=['GET', 'POST'])
def add_ingredient():
    if request.method == 'POST':
        name = request.form.get('name')
        total_cost = float(request.form.get('total_cost'))
        total_quantity = float(request.form.get('total_quantity'))
        unit = request.form.get('unit')
        
        new_ingredient = Ingredient(
            name=name,
            total_cost=total_cost,
            total_quantity=total_quantity,
            unit=unit
        )
        db.session.add(new_ingredient)
        db.session.commit()
        
        flash('เพิ่มวัตถุดิบสำเร็จ!', 'success')
        return redirect(url_for('ingredient.list_ingredients'))
    
    return render_template('ingredient/add.html')

# แก้ไขวัตถุดิบ
@ingredient_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    
    if request.method == 'POST':
        ingredient.name = request.form.get('name')
        ingredient.total_cost = float(request.form.get('total_cost'))
        ingredient.total_quantity = float(request.form.get('total_quantity'))
        ingredient.unit = request.form.get('unit')
        
        db.session.commit()
        flash('แก้ไขวัตถุดิบสำเร็จ!', 'success')
        return redirect(url_for('ingredient.list_ingredients'))
    
    return render_template('ingredient/edit.html', ingredient=ingredient)

# ลบวัตถุดิบ
@ingredient_bp.route('/delete/<int:id>', methods=['POST'])
def delete_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    flash('ลบวัตถุดิบสำเร็จ!', 'success')
    return redirect(url_for('ingredient.list_ingredients'))

# จัดการสูตรอาหาร (ต่อเมนู)
@ingredient_bp.route('/recipe/<int:menu_id>', methods=['GET', 'POST'])
def manage_recipe(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    ingredients = Ingredient.query.all()
    recipes = Recipe.query.filter_by(menu_id=menu_id).all()
    
    if request.method == 'POST':
        # ลบสูตรเก่า
        Recipe.query.filter_by(menu_id=menu_id).delete()
        
        # เพิ่มสูตรใหม่
        ingredient_ids = request.form.getlist('ingredient_id')
        grams_per_dish = request.form.getlist('grams_per_dish')  # ✅ เปลี่ยนชื่อ
        
        for i, ing_id in enumerate(ingredient_ids):
            if ing_id and grams_per_dish[i]:
                recipe = Recipe(
                    menu_id=menu_id,
                    ingredient_id=int(ing_id),
                    grams_per_dish=float(grams_per_dish[i])  # ✅ เปลี่ยนชื่อ
                )
                db.session.add(recipe)
        
        db.session.commit()
        flash('บันทึกสูตรอาหารสำเร็จ!', 'success')
        return redirect(url_for('menu.list_menu'))
    
    return render_template('ingredient/recipe.html', 
                         menu=menu, 
                         ingredients=ingredients, 
                         recipes=recipes)