from flask import Blueprint, render_template, request, session, flash
from .models import Product
from . import db, os
import requests

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

        elif filename != "" and img_link != "":
            flash(
                'You can\'t have both link and file for the image, choose only one.', category='error')
            return render_template("add_product.html")
        elif img_link == "" and filename != "":
            img_file.save(filename)

            new_product = Product(name=product_name, price=product_price,
                                  image='\\website\\' + filename, info=product_info)

            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', category='success')
            return render_template('add_product.html')
        elif img_link != "" and filename == "":
            # download the link and save it in the database
            response = requests.get(img_link)

            content_type = response.headers['Content-Type']
            ext = content_type.split('/')[-1]

            number = 1
            while os.path.isfile(f'image-{number}.{ext}'):
                number += 1
            filename = f'image-{number}.{ext}'
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)

                new_product = Product(name=product_name, price=product_price,
                                      image='\\website\\'+filename, info=product_info)

                db.session.add(new_product)
                db.session.commit()
                flash('Product added successfully!', category='success')
                return render_template('add_product.html')

            else:
                flash(
                    'Image Link is Invalid! Try another link or upload an image file.', category='error')

    return render_template('add_product.html')
