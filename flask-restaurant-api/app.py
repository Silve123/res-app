from flask import Flask, jsonify, request
from db import Database
from order import Order
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows all origins, you can configure it for specific origins if needed

# SQLite database name
db_name = 'orders.db'

# Create a database connection
db = Database(db_name)

# Create an Order instance
order_handler = Order(db)

# Route to create an order
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    customer_name = data['customer_name']
    customer_email = data['customer_email']  # Include customer_email from the request
    meals = data['meals']

    # Create the order with default values for order_status and progress_id
    order_id = order_handler.create_order(customer_name, customer_email, meals)

    if order_id is not None:
        return jsonify({"message": "Order created successfully", "order_id": order_id}), 201
    else:
        return jsonify({"message": "Failed to create order"}), 500



# Route to get all orders
@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = order_handler.get_orders()
    return jsonify(orders)


@app.route('/api/meals', methods=['GET'])
def get_meals():
    try:
        # Query all meals from the database
        query = "SELECT meal_id, meal_name, meal_type, description, price FROM meals"
        meals = db.execute_select_query(query)

        # Convert the database results to a list of dictionaries
        meal_list = []
        for meal in meals:
            meal_dict = {
                "meal_id": meal[0],
                "meal_name": meal[1],
                "meal_type": meal[2],
                "description": meal[3],
                "price": meal[4]
            }
            meal_list.append(meal_dict)

        # Return the meals as JSON
        return jsonify(meal_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:customer_id>', methods=['GET'])
def get_orders_for_customer(customer_id):
    try:
        # Query orders for the given customer_id from the database
        query = """
            SELECT o.order_id, o.customer_name, o.customer_email, o.order_time, o.status_id, o.progress_id
            FROM orders o
            WHERE o.customer_id = ?
        """
        orders = db.execute_select_query(query, (customer_id,))

        # Convert the database results to a list of dictionaries
        order_list = []
        for order in orders:
            order_dict = {
                "order_id": order[0],
                "customer_name": order[1],
                "customer_email": order[2],
                "order_time": order[3],
                "status_id": order[4],
                "progress_id": order[5],
            }
            order_list.append(order_dict)

        # Return the orders as JSON
        return jsonify(order_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/delete/<int:customer_id>/<int:order_id>', methods=['DELETE'])
def delete_order_for_customer(customer_id, order_id):
    try:
        # Check if the order with the given order_id belongs to the specified customer_id
        query = """
            SELECT customer_id
            FROM orders
            WHERE order_id = ? AND customer_id = ?
        """
        result = db.execute_select_query(query, (order_id, customer_id))

        if not result:
            return jsonify({"message": "Order not found for the specified customer"}), 404

        # Delete the order from the database
        delete_query = "DELETE FROM orders WHERE order_id = ?"
        db.execute_query(delete_query, (order_id,))

        return jsonify({"message": "Order deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/meals/order/<int:order_id>', methods=['GET'])
def get_meals_for_order(order_id):
    try:
        # Query meals for the given order_id from the database
        query = """
            SELECT m.meal_id, m.meal_name, m.meal_type, m.description, m.price
            FROM meals m
            INNER JOIN order_meals om ON m.meal_id = om.meal_id
            WHERE om.order_id = ?
        """
        meals = db.execute_select_query(query, (order_id,))

        # Convert the database results to a list of dictionaries
        meal_list = []
        for meal in meals:
            meal_dict = {
                "meal_id": meal[0],
                "meal_name": meal[1],
                "meal_type": meal[2],
                "description": meal[3],
                "price": meal[4]
            }
            meal_list.append(meal_dict)

        # Return the meals as JSON
        return jsonify(meal_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
