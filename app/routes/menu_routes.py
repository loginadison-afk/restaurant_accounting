from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Menu

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

@menu_bp.route('/')
def list_menu():
    """แสดงรายการเมนูทั้งหมด"""
    menus = Menu.query.all()
    return render_template('menu/list.html', menus=menus)

@menu_bp.route('/add', methods=['GET', 'POST'])
def add_menu():
    """เพิ่มเมนูใหม่"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        
        new_menu = Menu(name=name, price=price, category=category)
        db.session.add(new_menu)
        db.session.commit()
        
        flash('เพิ่มเมนูสำเร็จ! ไปกำหนดสูตรอาหารกันเลย', 'success')
        return redirect(url_for('ingredient.manage_recipe', menu_id=new_menu.id))
    
    return render_template('menu/add.html')

@menu_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu(id):
    """แก้ไขเมนู"""
    menu = Menu.query.get_or_404(id)
    
    if request.method == 'POST':
        menu.name = request.form.get('name')
        menu.price = float(request.form.get('price'))
        menu.category = request.form.get('category')
        
        db.session.commit()
        flash('แก้ไขเมนูสำเร็จ!', 'success')
        return redirect(url_for('menu.list_menu'))
    
    return render_template('menu/edit.html', menu=menu)

@menu_bp.route('/delete/<int:id>', methods=['POST'])
def delete_menu(id):
    """ลบเมนู"""
    menu = Menu.query.get_or_404(id)
    db.session.delete(menu)
    db.session.commit()
    flash('ลบเมนูสำเร็จ!', 'success')
    return redirect(url_for('menu.list_menu'))