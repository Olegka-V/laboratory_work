from flask import Flask, request, jsonify
from functools import wraps
import bcrypt
from uuid import uuid4

app = Flask(__name__)

# Дані для базової аутентифікації
USERS = {"admin": bcrypt.hashpw(b"password", bcrypt.gensalt()).decode()}

# Каталог товарів
items = {}

# Декоратор для базової аутентифікації
def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not bcrypt.checkpw(auth.password.encode(), USERS.get(auth.username, "").encode()):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/items', methods=['GET', 'POST'])
@authenticate
def manage_items():
    if request.method == 'GET':
        return jsonify(items)
    elif request.method == 'POST':
        data = request.get_json()
        if not data or "name" not in data or "price" not in data or "size" not in data:
            return jsonify({"message": "Invalid input"}), 400
        new_id = str(uuid4())  # Використання унікальних UUID
        items[new_id] = data
        return jsonify({"message": "Item added", "item": items[new_id]}), 201

@app.route('/items/<string:item_id>', methods=['GET', 'PUT', 'DELETE'])
@authenticate
def manage_item(item_id):
    if item_id not in items:
        return jsonify({"message": "Item not found"}), 404
    
    if request.method == 'GET':
        return jsonify(items[item_id])
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input"}), 400
        items[item_id].update(data)
        return jsonify({"message": "Item updated", "item": items[item_id]})
    elif request.method == 'DELETE':
        del items[item_id]
        return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(port=8000)
