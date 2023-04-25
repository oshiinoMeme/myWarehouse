from flask import Flask, render_template, request, redirect, url_for
from forms import DeleteInventoryForm, DeleteDispatchForm, DeleteReceivingForm, LoginForm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import LoginManager
from flask_security import UserMixin, RoleMixin
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse2.db'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Employees(db.Model):
    employees_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Supplier(db.Model):
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), primary_key=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)

class Storage_location(db.Model):
    storage_id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    shelf = db.Column(db.Integer, nullable=False)

class Product(db.Model):
    product_name = db.Column(db.String(50), primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    storage_type = db.Column(db.String(50), nullable=False)

class Inventory(db.Model):
    inventory_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), db.ForeignKey('product.product_name'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    storage_id = db.Column(db.Integer, db.ForeignKey('storage_location.storage_id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('inventory', lazy=True))
    storage_location = db.relationship('Storage_location', backref=db.backref('Inventory', lazy=True))

class Receiving(db.Model):
    receiving_id = db.Column(db.Integer, primary_key=True)
    employees_id = db.Column(db.Integer, db.ForeignKey('employees.employees_id'), nullable=False)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.supply_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(100))
    employees = db.relationship('Employees', backref=db.backref('Receiving', lazy=True))

class Dispatch(db.Model):
    dispatch_id = db.Column(db.Integer, primary_key=True)
    employees_id = db.Column(db.Integer, db.ForeignKey('employees.employees_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(100))
    employees = db.relationship('Employees', backref=db.backref('Dispatch', lazy=True))

class Customer(db.Model):
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), primary_key=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)

class Supply(db.Model):
    supply_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), db.ForeignKey('product.product_name'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplier_email = db.Column(db.String, db.ForeignKey('supplier.email'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    product = db.relationship('Product', backref=db.backref('supply', lazy=True))
    supplier = db.relationship('Supplier', backref=db.backref('supply', lazy=True))

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), db.ForeignKey('product.product_name'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    customer_email = db.Column(db.String, db.ForeignKey('customer.email'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    product = db.relationship('Product', backref=db.backref('order', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('order', lazy=True))

roles_user = db.Table('roles_user',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_user ,backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        return role in [r.name for r in self.roles]

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

import adm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('search'))

    return render_template('login.html', form=form)

@app.route('/admin')
@login_required
def admin():
    if not current_user.has_role('admin'):
        return redirect(url_for('login'))
    return redirect('/admin/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def navi():
    return render_template('search.html')

@app.route('/search')
@login_required
def search():
    return render_template('search.html')

@app.route('/search_product')
@login_required
def search_product():
    search_term = request.args.get('search_term')
    product = Product.query.filter_by(product_name=search_term).first()
    if not product:
        return render_template('search_results.html', product=None)

    inventory_rows = Inventory.query.filter_by(product_name=product.product_name).all()
    order_rows = Order.query.filter_by(product_name=product.product_name).all()
    supply_rows = Supply.query.filter_by(product_name=product.product_name).all()
    return render_template('search_results.html', product=product, inventory_rows=inventory_rows, order_rows=order_rows, supply_rows=supply_rows)

@app.route('/receiving')
@login_required
def receiving():
    q = request.args.get('q')
    supply_list = Supply.query.all()
    if q:
        receiving_list = Receiving.query.filter(Receiving.status.contains(q)).all()
    else:
        receiving_list = Receiving.query.all()

    receiving_supply_ids = [d.supply_id for d in receiving_list if d.status == 'Supply Inventory']
    pending_supply = [o for o in supply_list if o.supply_id not in receiving_supply_ids]
    return render_template('receiving/receiving.html', supply=pending_supply, receiving=receiving_list)

@app.route('/receiving/add', methods=['GET', 'POST'])
@login_required
def add_receiving():
    if request.method == 'POST':
        employees_id = request.form['employees_id']
        supply_id = request.form['supply_id']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        status = request.form['status']
        new_receiving = Receiving(employees_id=employees_id, supply_id=supply_id, date=date, status=status)
        db.session.add(new_receiving)
        db.session.commit()
        return redirect(url_for('receiving'))
    else:
        employees = Employees.query.all()
        supply = Supply.query.all()
        return render_template('receiving/add_receiving.html', receiving=receiving, employees=employees, supply=supply)

@app.route('/receiving/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_receiving(id):
    receiving = Receiving.query.get_or_404(id)
    if request.method == 'POST':
        receiving.employees_id = request.form['employees_id']
        receiving.status = request.form['status']
        db.session.commit()
        return redirect(url_for('receiving'))
    else:
        employees = Employees.query.all()
        return render_template('receiving/edit_receiving.html', receiving=receiving, employees=employees)

@app.route('/receiving/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_receiving(id):
    receiving = Receiving.query.get_or_404(id)
    form = DeleteReceivingForm()
    if request.method == 'POST':
        db.session.delete(receiving)
        db.session.commit()
        return redirect(url_for('receiving'))
    else:
        return render_template('receiving/delete_receiving.html', form=form, receiving=receiving)

@app.route('/inventory')
@login_required
def inventory():
    q = request.args.get('q')
    if q:
        inventory_list = Inventory.query.join(Product).filter(Product.product_name.contains(q)).all()
    else:
        inventory_list = Inventory.query.all()
    return render_template('inventory/inventory.html', inventory=inventory_list)

@app.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_inventory():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        storage_id = request.form['storage_id']
        new_inventory = Inventory(product_name=product_name, quantity=quantity, storage_id=storage_id)
        db.session.add(new_inventory)
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        products = Product.query.all()
        storage_locations = Storage_location.query.all()
        return render_template('inventory/add_inventory.html', products=products, storage_locations=storage_locations)

@app.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    if request.method == 'POST':
        inventory.product_name = request.form['product_name']
        inventory.quantity = request.form['quantity']
        inventory.storage_id = request.form['storage_id']
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        products = Product.query.all()
        storage_locations = Storage_location.query.all()
        return render_template('inventory/edit_inventory.html', inventory=inventory, products=products, storage_locations=storage_locations)

@app.route('/inventory/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    form = DeleteInventoryForm()
    if request.method == 'POST':
        db.session.delete(inventory)
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        return render_template('inventory/delete_inventory.html', form=form, inventory=inventory)

@app.route('/dispatch')
@login_required
def dispatch():
    q = request.args.get('q')
    order_list = Order.query.all()
    if q:
        dispatch_list = Dispatch.query.filter(Dispatch.status.contains(q)).all()
    else:
        dispatch_list = Dispatch.query.all()
    
    dispatched_order_ids = [d.order_id for d in dispatch_list if d.status == 'Order Sent']
    pending_orders = [o for o in order_list if o.order_id not in dispatched_order_ids]
    return render_template('dispatch/dispatch.html', order=pending_orders, dispatch=dispatch_list)

@app.route('/dispatch/add', methods=['GET', 'POST'])
@login_required
def add_dispatch():
    if request.method == 'POST':
        employees_id = request.form['employees_id']
        order_id = request.form['order_id']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        status = request.form['status']
        new_dispatch = Dispatch(employees_id=employees_id, order_id=order_id, date=date, status=status)
        db.session.add(new_dispatch)
        db.session.commit()
        return redirect(url_for('dispatch'))
    else:
        employees = Employees.query.all()
        orders = Order.query.all()
        return render_template('dispatch/add_dispatch.html', dispatch=dispatch, employees=employees, orders=orders)

@app.route('/dispatch/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dispatch(id):
    dispatch = Dispatch.query.get_or_404(id)
    if request.method == 'POST':
        dispatch.employees_id = request.form['employees_id']
        dispatch.status = request.form['status']
        db.session.commit()
        return redirect(url_for('dispatch'))
    else:
        employees = Employees.query.all()
        return render_template('dispatch/edit_dispatch.html', dispatch=dispatch, employees=employees)

@app.route('/dispatch/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_dispatch(id):
    dispatch = Dispatch.query.get_or_404(id)
    form = DeleteDispatchForm()
    if request.method == 'POST':
        db.session.delete(dispatch)
        db.session.commit()
        return redirect(url_for('dispatch'))
    else:
        return render_template('dispatch/delete_dispatch.html', form=form, dispatch=dispatch)

if __name__ == '__main__':
    app.run(debug=True)


