from flask import Flask, request, jsonify, render_template
from uuid import uuid4

app = Flask(__name__)

# In-memory storage for items
items = []

# Data model for an item
class Item:
    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(data['name'])
    items.append({'id': new_item.id, 'name': new_item.name})
    return jsonify({'message': 'Item added', 'item': new_item.__dict__}), 201

@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    for item in items:
        if item['id'] == item_id:
            item['name'] = data['name']
            return jsonify({'message': 'Item updated', 'item': item})
    return jsonify({'message': 'Item not found'}), 404

@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True)
