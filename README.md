# WAREHOUSE APPLICATION
This is a Flask app that allows users to manage their warehouse. Users can perform the following actions:

# Usage
Login: Only registered users can use this app. Users can log in by providing their email and password.
CRUD Receiving, Inventory, Dispatch: Users can perform Create, Read, Update, and Delete (CRUD) operations on the Receiving, Inventory, and Dispatch tables.
Receiving: Users can see supplies that are added by admin. If the user sets the status to "Supply Inventory," the supply will automatically be removed from the page. Users can search for the receiving by entering the status name on the "Search" field.
Dispatch: Users can see orders that are added by admin. If the user sets the status to "Order Sent," the order will automatically be removed from the page. Users can search for dispatch by entering the status name on the "Search" field.
Search a Product: Users can search for a product by navigating to http://localhost:5000/search, entering the name of the product they're looking for, and then clicking "Search."
Admins: Admin users can perform all the actions mentioned above, as well as the following:
Click on their email on the right side of the navbar to go to the admin page.
CRUD all other tables on the admin page, including Supply, Order, Employees, Suppliers, Customers, Product, and Storage_location.
To log out of the app, click on the "Logout" link in the navbar.

# How to Run the App
To run this app on your local machine, follow these steps:
1. On console clone this repository to your local machine.
2. Go to the app dir
3. Activate venv: "source venv/bin/activate"
4. Install libraries: "pip3 install -r requirements.txt"
5. then: "export FLASK_APP=app.py"
6. then: "flask run"
7. The app should now be running at http://localhost:5000.

# Technology Used
This app was built using Flask, a Python web framework, and SQLAlchemy, an Object-Relational Mapping (ORM) tool. The front-end was built using HTML, CSS, and Bootstrap.

# Contributing
Contributions are welcome! If you notice a bug or have an idea for a new feature, please submit an issue on GitHub or open a pull request with your changes.
