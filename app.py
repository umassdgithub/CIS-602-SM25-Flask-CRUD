from flask import Flask, request, jsonify, send_file

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

app = Flask(__name__,static_folder = "./static/dist",static_url_path = "")
CORS(app)

## Create database

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydatabase.db"

db = SQLAlchemy(app)



@app.route("/createDB",methods=["GET"])
def index():
    db.create_all()
    return jsonify({"msg":"database exists/created!"})

## Make the models

### Products
#### id
#### name
#### description
#### price
#### count
class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),primary_key = False,nullable=False)
    description = db.Column(db.Integer,primary_key = False,nullable=False)
    price = db.Column(db.Float,primary_key = False,nullable=False)
    count = db.Column(db.Integer,primary_key = False,nullable=False)

## CRUD
###Create
@app.route("/api/products",methods=["POST"])
def create_product():
    data = request.json
    product = Product(
        name = data["name"],
        description = data["description"],
        price = data["price"],
        count = data["count"]
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({ "msg" : "record added!" })

### Read
#### Query All

@app.route("/api/products",methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify([ {"id":p.id,
                      "name":p.name,
                      "description":p.description,
                      "price":p.price,
                      "count":p.count
                      } for p in products ])
#### Query one
@app.route("/api/products/<int:product_id>",methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify( {"id":product.id,
                      "name":product.name,
                      "description":product.description,
                      "price":product.price,
                      "count":product.count
                      })
    else:
        return jsonify({"msg": "no results found!"}),404

### Update
@app.route("/api/products/<int:product_id>",methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        data = request.json
        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.count = data["count"]
        db.session.commit()

        return jsonify({"msg":"update completed"}),201
    else:
        return jsonify({"msg": "no results found!"}),404

### Delete
@app.route("/api/products/<int:product_id>",methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()

        return jsonify({"msg":"delete completed"}),201
    else:
        return jsonify({"msg": "no results found!"}),404



@app.route("/")
def homepage():
    return jsonify({"msg":"refer to the readme.md file for the explanation."})




if __name__ == "__main__":
    app.run(debug=True,host= "0.0.0.0",port = 5000)

 