from flask import Blueprint, render_template, request, session, flash
from .models import Product
from . import db

views = Blueprint("views", __name__)


@views.route("/add_product", methods=['GET', 'POST'])
def add_product():
    filename = ""
    if request.method == "POST":
        product_name = request.form.get("product_name")
        product_price = request.form.get("product_price")
        product_info = request.form.get("product_info")
        img_file = request.files['img_file']
        img_link = request.form.get("img_link")
        filename = img_file.filename
        # print(filename)

        product = Product.query.filter_by(name=product_name).first()

        if product:
            flash('This Product Already Exists!', category="error")

        elif len(product_name) < 4:
            flash('Product\'s name must be greater than 3 characters.',
                  category='error')
        elif product_price == "" or float(product_price) <= 0:
            flash('The price must be greater than 0$.', category='error')
        elif filename == "" and img_link == "":
            flash('Product\'s image should not be empty.', category='error')

        else:
            if filename != "" and img_link != "":
                flash(
                    'You can\'t have both link and file for the image, choose only one.', category='error')
                return render_template("add_product.html", filename="")

            try:
                new_product = Product(name=product_name, price=product_price,
                                      image=filename if filename != "" and img_link == "" else img_link, info=product_info)
                db.session.add(new_product)
                db.session.commit()
            except:
                flash('This Product Already Exists!', category="error")

            else:
                flash('Product added successfully!', category='success')
                return render_template('add_product.html', filename=filename)

    return render_template('add_product.html', filename=filename)
