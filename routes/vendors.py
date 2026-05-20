from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Vendor
from routes.__init__ import login_required

vendors_bp = Blueprint('vendors', __name__, template_folder='../templates')


@vendors_bp.route('/')
@login_required
def list():
    vendors = Vendor.query.order_by(Vendor.name).all()
    return render_template('vendors/list.html', vendors=vendors)


@vendors_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        vendor = Vendor(
            name=request.form['name'],
            contact_person=request.form.get('contact_person'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            notes=request.form.get('notes'),
        )
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor created successfully', 'success')
        return redirect(url_for('vendors.list'))
    return render_template('vendors/form.html', vendor=None)


@vendors_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    vendor = Vendor.query.get_or_404(id)
    if request.method == 'POST':
        vendor.name = request.form['name']
        vendor.contact_person = request.form.get('contact_person')
        vendor.email = request.form.get('email')
        vendor.phone = request.form.get('phone')
        vendor.address = request.form.get('address')
        vendor.notes = request.form.get('notes')
        db.session.commit()
        flash('Vendor updated successfully', 'success')
        return redirect(url_for('vendors.list'))
    return render_template('vendors/form.html', vendor=vendor)


@vendors_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    vendor = Vendor.query.get_or_404(id)
    db.session.delete(vendor)
    db.session.commit()
    flash('Vendor deleted successfully', 'success')
    return redirect(url_for('vendors.list'))
