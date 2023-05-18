from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/add_product")
def add_product():
    return render_template("add_product.html")