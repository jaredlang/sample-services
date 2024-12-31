from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for products
products = [{
    "id": "p1",
    "manufacturer": "Apple",
    "model": "iPhone 16", 
    "size": "128GB"
}, {
    "id": "p2",
    "manufacturer": "Apple",
    "model": "iPhone 15", 
    "size": "128GB"
}, {
    "id": "p3",
    "manufacturer": "Samsumg",
    "model": "Galaxy 24", 
    "size": "256GB"
}]

# Utility function to find a product by ID
def find_product_by_id(product_id):
    return next((product for product in products if product['id'] == product_id), None)

@app.route('/', methods=['GET'])
def service_health():
    return 'live', 200

@app.route('/products', methods=['GET'])
def get_all_products():
    """Return all products."""
    return jsonify(products), 200

@app.route('/products/<string:productId>', methods=['GET'])
def get_product_by_id(productId):
    """Find product by Id."""
    product = find_product_by_id(productId)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/products/<string:productId>', methods=['DELETE'])
def delete_product(productId):
    """Delete a product from the inventory."""
    global products
    product = find_product_by_id(productId)
    if product:
        products = [p for p in products if p['id'] != productId]
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['PUT'])
def update_product():
    """Update an existing product."""
    product_data = request.get_json()
    product = find_product_by_id(product_data.get('id'))
    if product:
        product.update(product_data)
        return jsonify({"message": "Product updated", "product": product}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def add_product():
    """Add a new product."""
    product_data = request.get_json()
    product_id = len(products)+1
    product_data["id"]=f"p-{product_id}"
    products.append(product_data)
    return jsonify({"message": "Product added", "product": product_data}), 201

@app.route('/products/findByModel', methods=['GET'])
def find_products_by_model():
    """Find products by model."""
    model = request.args.get('model')
    if model:
        filtered_products = [product for product in products if product['model'] == model]
        return jsonify(filtered_products), 200
    return jsonify({"error": "Model not specified"}), 400

if __name__ == '__main__':
    app.run(debug=True)
