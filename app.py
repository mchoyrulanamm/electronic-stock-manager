import os
from flask import Flask, render_template
from config import Config
from models import db, Component, Category, Vendor, StockMovement, User
from routes.__init__ import login_required

from routes.vendors import vendors_bp
from routes.categories import categories_bp
from routes.components import components_bp
from routes.movements import movements_bp
from routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)
        db.create_all()

        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

    app.register_blueprint(vendors_bp, url_prefix='/vendors')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(components_bp, url_prefix='/components')
    app.register_blueprint(movements_bp, url_prefix='/movements')
    app.register_blueprint(auth_bp)

    @app.route('/')
    @login_required
    def index():
        low_stock = Component.query.filter(Component.stock_qty < Component.min_stock).all()
        total_components = Component.query.count()
        total_categories = Category.query.count()
        total_vendors = Vendor.query.count()
        recent_movements = StockMovement.query\
            .order_by(StockMovement.created_at.desc())\
            .limit(10).all()
        return render_template('index.html',
                               low_stock=low_stock,
                               total_components=total_components,
                               total_categories=total_categories,
                               total_vendors=total_vendors,
                               recent_movements=recent_movements)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host="0.0.0.0")
