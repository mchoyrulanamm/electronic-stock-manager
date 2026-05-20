from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, StockMovement, Component
from routes.__init__ import login_required

movements_bp = Blueprint('movements', __name__, template_folder='../templates')


@movements_bp.route('/')
@login_required
def list():
    component_id = request.args.get('component_id', '').strip()
    query = StockMovement.query
    if component_id:
        query = query.filter(StockMovement.component_id == int(component_id))
    movements = query.order_by(StockMovement.created_at.desc()).all()
    components = Component.query.order_by(Component.name).all()
    return render_template('movements/list.html',
                           movements=movements,
                           components=components,
                           selected_component=component_id)


@movements_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        component_id = int(request.form['component_id'])
        movement_type = request.form['movement_type']
        quantity = int(request.form['quantity'])
        note = request.form.get('note')

        quantity_change = quantity if movement_type == 'in' else -quantity

        component = Component.query.get_or_404(component_id)
        component.stock_qty += quantity_change

        movement = StockMovement(
            component_id=component_id,
            quantity_change=quantity_change,
            movement_type=movement_type,
            note=note,
        )
        db.session.add(movement)
        db.session.commit()
        flash('Stock movement recorded successfully', 'success')
        return redirect(url_for('movements.list'))

    components = Component.query.order_by(Component.name).all()
    preselected = request.args.get('component_id', type=int)
    return render_template('movements/form.html',
                           components=components,
                           preselected=preselected)
