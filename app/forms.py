from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, SubmitField, SelectField, validators, PasswordField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

class RoleRestrictedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

class AddInventoryForm(FlaskForm):
    product_name = IntegerField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    storage_id = IntegerField('Storage Name', validators=[DataRequired()])
    submit = SubmitField('Add Inventory')


class EditInventoryForm(FlaskForm):
    product_name = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    storage_id = IntegerField('Storage ID', validators=[DataRequired()])
    submit = SubmitField('Update Inventory')

class DeleteInventoryForm(FlaskForm):
    submit = SubmitField('Delete Inventory')

class DispatchForm(FlaskForm):
    employees_id = StringField('Employees ID', validators=[DataRequired(), Length(max=50)])
    order_id = StringField('Order ID', validators=[DataRequired(), Length(max=50)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[('delivered', 'Delivered'), ('in transit', 'In Transit'), ('arrived', 'Arrived')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteDispatchForm(FlaskForm):
    submit = SubmitField('Delete Dispatch')

class ReceivingForm(FlaskForm):
    employees_id = StringField('Employees ID', validators=[DataRequired(), Length(max=50)])
    supply_id = StringField('Supply ID', validators=[DataRequired(), Length(max=50)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[('in transit', 'In Transit'), ('pending', 'Pending')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteReceivingForm(FlaskForm):
    submit = SubmitField('Delete Receiving')

class OrderAdmin(RoleRestrictedModelView):
    column_list = ('order_id', 'product_name', 'quantity', 'customer_email', 'date')
    form_columns = ('product', 'quantity', 'customer', 'date')
    column_sortable_list = ('order_id', 'product_name', 'quantity', 'customer_email', 'date')
    form_args = {
        'product': {'label': 'Product', 'validators': [validators.DataRequired()]},
        'quantity': {'label': 'Quantity', 'validators': [validators.DataRequired()]},
        'customer': {'label': 'Customer', 'validators': [validators.DataRequired()]},
        'date': {'label': 'Date', 'validators': [validators.DataRequired()]},
    }

class SupplyAdmin(RoleRestrictedModelView):
    column_list = ('supply_id', 'product_name', 'quantity', 'supplier_email', 'date')
    form_columns = ('product', 'quantity', 'supplier', 'date')
    column_sortable_list = ('supply_id', 'product_name', 'quantity', 'supplier_email', 'date')
    form_args = {
        'product': {'label': 'Product', 'validators': [validators.DataRequired()]},
        'quantity': {'label': 'Quantity', 'validators': [validators.DataRequired()]},
        'supplier': {'label': 'Supplier', 'validators': [validators.DataRequired()]},
        'date': {'label': 'Date', 'validators': [validators.DataRequired()]},
    }

class SupplierAdmin(RoleRestrictedModelView):
    column_list = ('name', 'email', 'phone', 'address')
    form_columns = ('name', 'email', 'phone', 'address')
    column_sortable_list = ('name', 'email', 'phone', 'address')
    form_args = {
        'name': {'label': 'Name', 'validators': [validators.DataRequired()]},
        'email': {'label': 'Email', 'validators': [validators.DataRequired(), validators.Email()]},
        'phone': {'label': 'Phone', 'validators': [validators.DataRequired()]},
        'address': {'label': 'Address', 'validators': [validators.DataRequired()]},
    }


class CustomerAdmin(RoleRestrictedModelView):
    column_list = ('name', 'email', 'phone', 'address')
    form_columns = ('name', 'email', 'phone', 'address')
    column_sortable_list = ('name', 'email', 'phone', 'address')
    form_args = {
        'name': {'label': 'Name', 'validators': [validators.DataRequired()]},
        'email': {'label': 'Email', 'validators': [validators.DataRequired(), validators.Email()]},
        'phone': {'label': 'Phone', 'validators': [validators.DataRequired()]},
        'address': {'label': 'Address', 'validators': [validators.DataRequired()]},
    }

class ProductAdmin(RoleRestrictedModelView):
    column_list = ('product_name', 'description', 'storage_type')
    form_columns = ('product_name', 'description', 'storage_type')
    column_sortable_list = ('product_name', 'description', 'storage_type')
    form_args = {
        'product_name': {'label': 'Product Name', 'validators': [validators.DataRequired()]},
        'description': {'label': 'Description', 'validators': [validators.DataRequired()]},
        'storage_type': {'label': 'Storage Type', 'validators': [validators.DataRequired()]},
    }

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Login')
