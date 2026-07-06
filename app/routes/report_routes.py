from flask import Blueprint, render_template, request
from app import db
from app.models import Menu, DailySale, Ingredient
from datetime import datetime, timedelta, date
from calendar import monthrange

report_bp = Blueprint('report', __name__, url_prefix='/')

def get_dashboard_data():
    """ฟังก์ชันดึงข้อมูล Dashboard"""
    total_menus = Menu.query.count()
    total_sales = DailySale.query.count()
    total_ingredients = Ingredient.query.count()
    
    all_sales = DailySale.query.all()
    total_revenue = sum(s.revenue for s in all_sales)
    total_cost = sum(s.total_cost for s in all_sales)
    total_profit = sum(s.profit for s in all_sales)
    
    # แยกตามประเภท
    delivery_sales = DailySale.query.join(Menu).filter(Menu.category == 'delivery').all()
    instore_sales = DailySale.query.join(Menu).filter(Menu.category == 'instore').all()
    
    delivery_revenue = sum(s.revenue for s in delivery_sales)
    delivery_cost = sum(s.total_cost for s in delivery_sales)
    delivery_profit = sum(s.profit for s in delivery_sales)
    
    instore_revenue = sum(s.revenue for s in instore_sales)
    instore_cost = sum(s.total_cost for s in instore_sales)
    instore_profit = sum(s.profit for s in instore_sales)
    
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    delivery_margin = (delivery_profit / delivery_revenue * 100) if delivery_revenue > 0 else 0
    instore_margin = (instore_profit / instore_revenue * 100) if instore_revenue > 0 else 0
    
    # หาเมนูที่กำไรสูงสุดและขาดทุนสูงสุด
    menus_with_profit = []
    for menu in Menu.query.all():
        sales = DailySale.query.filter_by(menu_id=menu.id).all()
        total_qty = sum(s.quantity for s in sales)
        if total_qty > 0:
            profit = sum(s.profit for s in sales)
            menus_with_profit.append({
                'name': menu.name,
                'profit': profit,
                'category': 'ส่ง' if menu.category == 'delivery' else 'หน้าร้าน'
            })
    
    best_menu = max(menus_with_profit, key=lambda x: x['profit']) if menus_with_profit else None
    worst_menu = min(menus_with_profit, key=lambda x: x['profit']) if menus_with_profit else None
    
    return {
        'total_menus': total_menus,
        'total_sales': total_sales,
        'total_ingredients': total_ingredients,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'profit_margin': profit_margin,
        'delivery_revenue': delivery_revenue,
        'delivery_cost': delivery_cost,
        'delivery_profit': delivery_profit,
        'delivery_margin': delivery_margin,
        'instore_revenue': instore_revenue,
        'instore_cost': instore_cost,
        'instore_profit': instore_profit,
        'instore_margin': instore_margin,
        'best_menu': best_menu,
        'worst_menu': worst_menu
    }

# ✅ ฟังก์ชันใหม่: ดึงข้อมูลตามช่วงเวลา
def get_sales_by_date_range(start_date, end_date):
    """ดึงยอดขายในช่วงวันที่"""
    sales = DailySale.query.filter(
        DailySale.sale_date >= start_date,
        DailySale.sale_date <= end_date
    ).all()
    
    revenue = sum(s.revenue for s in sales)
    cost = sum(s.total_cost for s in sales)
    profit = sum(s.profit for s in sales)
    
    delivery_sales = [s for s in sales if s.menu.category == 'delivery']
    instore_sales = [s for s in sales if s.menu.category == 'instore']
    
    delivery_revenue = sum(s.revenue for s in delivery_sales)
    delivery_cost = sum(s.total_cost for s in delivery_sales)
    delivery_profit = sum(s.profit for s in delivery_sales)
    
    instore_revenue = sum(s.revenue for s in instore_sales)
    instore_cost = sum(s.total_cost for s in instore_sales)
    instore_profit = sum(s.profit for s in instore_sales)
    
    return {
        'revenue': revenue,
        'cost': cost,
        'profit': profit,
        'delivery_revenue': delivery_revenue,
        'delivery_cost': delivery_cost,
        'delivery_profit': delivery_profit,
        'instore_revenue': instore_revenue,
        'instore_cost': instore_cost,
        'instore_profit': instore_profit,
        'total_sales': len(sales)
    }

# ✅ หน้า Dashboard (หน้าแรก)
@report_bp.route('/')
def dashboard():
    data = get_dashboard_data()
    return render_template('index.html', **data)

# ✅ หน้ารายงานรายสัปดาห์
@report_bp.route('/report/weekly')
def weekly_report():
    today = date.today()
    start_date = today - timedelta(days=7)
    end_date = today
    
    data = get_sales_by_date_range(start_date, end_date)
    return render_template('report/weekly.html', 
                         start_date=start_date,
                         end_date=end_date,
                         **data)

# ✅ หน้ารายงานรายเดือน
@report_bp.route('/report/monthly')
def monthly_report():
    today = date.today()
    start_date = date(today.year, today.month, 1)
    last_day = monthrange(today.year, today.month)[1]
    end_date = date(today.year, today.month, last_day)
    
    data = get_sales_by_date_range(start_date, end_date)
    return render_template('report/monthly.html', 
                         start_date=start_date,
                         end_date=end_date,
                         month_name=today.strftime('%B %Y'),
                         **data)

# ✅ หน้ารายงานเลือกเอง
@report_bp.route('/report/custom', methods=['GET', 'POST'])
def custom_report():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        data = get_sales_by_date_range(start_date, end_date)
        return render_template('report/custom.html', 
                             start_date=start_date,
                             end_date=end_date,
                             **data)
    
    return render_template('report/custom.html', start_date=None, end_date=None)

@report_bp.route('/report')
def report_dashboard():
    data = get_dashboard_data()
    return render_template('index.html', **data)