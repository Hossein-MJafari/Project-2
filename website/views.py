from flask import Blueprint, render_template, request, session, flash
from . import sqlite3, current_directory
from os import path
import requests

views = Blueprint("views", __name__)


@views.route("/add_product", methods=['GET', 'POST'])
def add_product():
    filename = ""
    if request.method == "POST":
        product_name = request.form.get("product_name")
        product_price = request.form.get("product_price")
        product_stock = request.form.get("product_stock")
        product_info = request.form.get("product_info")
        img_file = request.files['img_file']
        img_link = request.form.get("img_link")
        filename = img_file.filename

        con = sqlite3.connect(current_directory + "\\mainDB.db")
        cur = con.cursor()
        table_name = 'products'

        select_query = f"SELECT * FROM {table_name} WHERE product_name=?;"
        result = cur.execute(select_query,(product_name,)).fetchall()

        if result:
            flash(
                f'The Product {product_name} Already Exists!', category="error")

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
            img_file.save("website\\" + filename)

            insert_query = f"""
            INSERT INTO {table_name} (product_name, product_price, stock, image, description)
            VALUES (?, ?, ?, ?, ?);
            """

            cur.execute(insert_query, (product_name,
                        product_price, product_stock, filename, product_info))
            con.commit()
            flash('Product added successfully!', category='success')
            return render_template('add_product.html')
        elif img_link != "" and filename == "":
            # download the link and save it in the database
            response = requests.get(img_link)

            content_type = response.headers['Content-Type']
            ext = content_type.split('/')[-1]

            number = 1
            while path.isfile(f'website\\image-{number}.{ext}'):
                number += 1

            filename = f'image-{number}.{ext}'

            if response.status_code == 200:
                with open('website\\' + filename, 'wb') as f:
                    f.write(response.content)

                insert_query = f"""
                INSERT INTO {table_name} (product_name, product_price, stock, image, description)
                VALUES (?, ?, ?, ?, ?);
                """

                cur.execute(insert_query, (product_name,
                            product_price, product_stock, filename, product_info))
                con.commit()
                flash('Product added successfully!', category='success')
                return render_template('add_product.html')

            else:
                flash(
                    'Image Link is Invalid! Try another link or upload an image file.', category='error')

        con.close()
    return render_template('add_product.html')
