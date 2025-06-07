from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session

# Sample products data (usually from DB)
products = {
    1: {"name": "Smartphone", "price": 699},
    2: {"name": "Laptop", "price": 1299},
    3: {"name": "Headphones", "price": 199},
}

@app.route("/")
def home():
    return render_template("home.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = products.get(product_id)
    if not product:
        return "Product not found", 404
    return render_template("product.html", product=product, product_id=product_id)

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    if product_id not in products:
        return "Product not found", 404
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = products.get(pid)
        if product:
            item_total = product["price"] * qty
            total += item_total
            cart_items.append({"product": product, "quantity": qty, "total": item_total})
    return render_template("cart.html", cart_items=cart_items, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)

