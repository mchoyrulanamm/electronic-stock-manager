from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Category
from routes.__init__ import login_required

categories_bp = Blueprint('categories', __name__, template_folder='../templates')


@categories_bp.route('/')
@login_required
def list():
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories/list.html', categories=categories)


@categories_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        category = Category(
            name=request.form['name'],
            description=request.form.get('description'),
        )
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully', 'success')
        return redirect(url_for('categories.list'))
    return render_template('categories/form.html', category=None)


@categories_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form.get('description')
        db.session.commit()
        flash('Category updated successfully', 'success')
        return redirect(url_for('categories.list'))
    return render_template('categories/form.html', category=category)


@categories_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully', 'success')
    return redirect(url_for('categories.list'))
