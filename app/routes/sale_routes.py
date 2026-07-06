from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Menu, DailySale
from datetime import datetime, date

sale_bp = Blueprint('sale', __name__, url_prefix='/sale')

@sale_bp.route('/')
def list_sales():
    """แสดงรายการยอดขายทั้งหมด"""
    sales = DailySale.query.order_by(DailySale.sale_date.desc()).all()
    return render_template('sale/list.html', sales=sales)

@sale_bp.route('/add', methods=['GET', 'POST'])
def add_sale():
    """บันทึกยอดขายประจำวัน"""
    menus = Menu.query.all()
    
    if request.method == 'POST':
        menu_id = int(request.form.get('menu_id'))
        quantity = int(request.form.get('quantity'))
        sale_date = request.form.get('sale_date')
        
        if not sale_date:
            sale_date = date.today()
        else:
            sale_date = datetime.strptime(sale_date, '%Y-%m-%d').date()
        
        # ตรวจสอบว่ามีข้อมูลขายวันนี้ของเมนูนี้หรือยัง
        existing = DailySale.query.filter_by(
            menu_id=menu_id,
            sale_date=sale_date
        ).first()
        
        if existing:
            existing.quantity += quantity
            flash(f'อัปเดตยอดขาย {existing.menu.name} เพิ่ม {quantity} จาน!', 'info')
        else:
            new_sale = DailySale(
                menu_id=menu_id,
                quantity=quantity,
                sale_date=sale_date
            )
            db.session.add(new_sale)
            flash('บันทึกยอดขายสำเร็จ!', 'success')
        
        db.session.commit()
        return redirect(url_for('sale.list_sales'))
    
    return render_template('sale/add.html', menus=menus, today=date.today())

# ✅ เพิ่มฟังก์ชันลบยอดขาย (ใหม่)
@sale_bp.route('/delete/<int:id>', methods=['POST'])
def delete_sale(id):
    """ลบยอดขาย"""
    sale = DailySale.query.get_or_404(id)
    menu_name = sale.menu.name
    quantity = sale.quantity
    
    db.session.delete(sale)
    db.session.commit()
    
    flash(f'ลบยอดขาย {menu_name} จำนวน {quantity} จาน สำเร็จ!', 'success')
    return redirect(url_for('sale.list_sales'))