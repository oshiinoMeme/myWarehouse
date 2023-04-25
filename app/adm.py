from app import *
from forms import OrderAdmin, SupplyAdmin, SupplierAdmin, ProductAdmin, CustomerAdmin, RoleRestrictedModelView
from flask_admin import Admin, expose
from flask_admin.base import BaseView

admin = Admin(app, name='WAREHOUSEE', template_mode='bootstrap3')

admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(SupplierAdmin(Supplier, db.session))
admin.add_view(SupplyAdmin(Supply, db.session))
admin.add_view(CustomerAdmin(Customer, db.session))
admin.add_view(OrderAdmin(Order, db.session))
admin.add_view(RoleRestrictedModelView(Employees, db.session))
admin.add_view(RoleRestrictedModelView(Storage_location, db.session))

class MyView(BaseView):
    @expose('/admin')
    def index(self):
        return self.render('admin/my_view.html')

    @expose('/back_to_app')
    def back_to_app(self):
        return redirect(url_for('index'))