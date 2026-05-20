from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Component, Category, Vendor
from routes.__init__ import login_required

components_bp = Blueprint('components', __name__, template_folder='../templates')


@components_bp.route('/')
@login_required
def list():
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category_id', '').strip()
    low_stock_only = request.args.get('low_stock', '').strip()

    query = Component.query

    if search:
        query = query.outerjoin(Vendor, Component.vendor_id == Vendor.id).filter(
            db.or_(
                Component.name.ilike(f'%{search}%'),
                Component.stock_code.ilike(f'%{search}%'),
                Component.vcode.ilike(f'%{search}%'),
                Component.value.ilike(f'%{search}%'),
                Vendor.name.ilike(f'%{search}%'),
            )
        )

    if category_id:
        query = query.filter(Component.category_id == int(category_id))

    if low_stock_only:
        query = query.filter(Component.stock_qty < Component.min_stock)

    components = query.order_by(Component.name).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template('components/list.html',
                           components=components,
                           categories=categories,
                           search=search,
                           selected_category=category_id,
                           low_stock_only=low_stock_only)


@components_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        component = Component(
            name=request.form['name'],
            stock_code=request.form.get('stock_code'),
            vcode=request.form.get('vcode'),
            description=request.form.get('description'),
            value=request.form.get('value'),
            package=request.form.get('package'),
            unit=request.form.get('unit', 'pcs'),
            stock_qty=int(request.form.get('stock_qty', 0)),
            min_stock=int(request.form.get('min_stock', 0)),
            purchase_url=request.form.get('purchase_url'),
            purchase_price=request.form.get('purchase_price', type=float) or None,
            selling_price=request.form.get('selling_price', type=float) or None,
            category_id=request.form.get('category_id', type=int) or None,
            vendor_id=request.form.get('vendor_id', type=int) or None,
        )
        db.session.add(component)
        db.session.commit()
        flash('Component created successfully', 'success')
        return redirect(url_for('components.list'))
    categories = Category.query.order_by(Category.name).all()
    vendors = Vendor.query.order_by(Vendor.name).all()
    return render_template('components/form.html',
                           component=None,
                           categories=categories,
                           vendors=vendors)


@components_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    component = Component.query.get_or_404(id)
    if request.method == 'POST':
        component.name = request.form['name']
        component.stock_code = request.form.get('stock_code')
        component.vcode = request.form.get('vcode')
        component.description = request.form.get('description')
        component.value = request.form.get('value')
        component.package = request.form.get('package')
        component.unit = request.form.get('unit', 'pcs')
        component.stock_qty = int(request.form.get('stock_qty', 0))
        component.min_stock = int(request.form.get('min_stock', 0))
        component.purchase_url = request.form.get('purchase_url')
        component.purchase_price = request.form.get('purchase_price', type=float) or None
        component.selling_price = request.form.get('selling_price', type=float) or None
        component.category_id = request.form.get('category_id', type=int) or None
        component.vendor_id = request.form.get('vendor_id', type=int) or None
        db.session.commit()
        flash('Component updated successfully', 'success')
        return redirect(url_for('components.list'))
    categories = Category.query.order_by(Category.name).all()
    vendors = Vendor.query.order_by(Vendor.name).all()
    return render_template('components/form.html',
                           component=component,
                           categories=categories,
                           vendors=vendors)


@components_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    component = Component.query.get_or_404(id)
    db.session.delete(component)
    db.session.commit()
    flash('Component deleted successfully', 'success')
    return redirect(url_for('components.list'))
