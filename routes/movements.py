from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models import db, StockMovement, Component
from routes.__init__ import login_required
from fpdf import FPDF
import io

movements_bp = Blueprint('movements', __name__, template_folder='../templates')


@movements_bp.route('/')
@login_required
def list():
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    query = StockMovement.query

    if date_from:
        query = query.filter(StockMovement.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(StockMovement.created_at <= datetime.strptime(date_to, '%Y-%m-%d').replace(hour=23, minute=59, second=59))

    movements = query.order_by(StockMovement.created_at.desc()).all()
    return render_template('movements/list.html',
                           movements=movements,
                           date_from=date_from,
                           date_to=date_to)


@movements_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        stock_code = request.form.get('stock_code', '').strip()
        movement_type = request.form['movement_type']
        quantity = int(request.form['quantity'])
        note = request.form.get('note')

        component = Component.query.filter_by(stock_code=stock_code).first()
        if not component:
            flash(f'Stock code "{stock_code}" not found', 'danger')
            return render_template('movements/form.html',
                                   stock_code=stock_code,
                                   movement_type=movement_type,
                                   quantity=quantity,
                                   note=note)

        quantity_change = quantity if movement_type == 'in' else -quantity
        component.stock_qty += quantity_change

        movement = StockMovement(
            component_id=component.id,
            quantity_change=quantity_change,
            movement_type=movement_type,
            note=note,
        )
        db.session.add(movement)
        db.session.commit()
        flash(f'Stock movement recorded: {component.name} ({stock_code})', 'success')
        return redirect(url_for('movements.list'))

    return render_template('movements/form.html')


@movements_bp.route('/export')
@login_required
def export():
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    query = StockMovement.query

    if date_from:
        query = query.filter(StockMovement.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(StockMovement.created_at <= datetime.strptime(date_to, '%Y-%m-%d').replace(hour=23, minute=59, second=59))

    movements = query.order_by(StockMovement.created_at.asc()).all()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Stock Movements Report', new_x='LMARGIN', new_y='NEXT', align='C')

    if date_from and date_to:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, f'Period: {date_from} to {date_to}', new_x='LMARGIN', new_y='NEXT', align='C')
    elif date_from:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, f'From: {date_from}', new_x='LMARGIN', new_y='NEXT', align='C')
    elif date_to:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, f'Until: {date_to}', new_x='LMARGIN', new_y='NEXT', align='C')

    pdf.ln(5)

    col_widths = [28, 50, 28, 18, 22, 44]
    headers = ['Date', 'Component', 'Stock Code', 'Type', 'Qty', 'Note']

    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(35, 139, 69)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 8)

    for m in movements:
        row = [
            m.created_at.strftime('%Y-%m-%d'),
            m.component.name[:20],
            m.component.stock_code or '-',
            m.movement_type.upper(),
            f"{'+' if m.quantity_change > 0 else ''}{m.quantity_change}",
            (m.note or '-')[:30],
        ]
        for i, val in enumerate(row):
            pdf.cell(col_widths[i], 7, val, border=1, align='C' if i in (0, 2, 3, 4) else 'L')
        pdf.ln()

    pdf.ln(5)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', new_x='LMARGIN', new_y='NEXT')

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, mimetype='application/pdf', as_attachment=True,
                     download_name=f'movements_{datetime.now().strftime("%Y%m%d")}.pdf')
