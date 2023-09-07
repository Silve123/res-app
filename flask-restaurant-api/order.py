class Order:
    def __init__(self, db):
        self.db = db

    def create_order(self, customer_name, customer_email, meals):
        # Check if the customer already exists
        customer_id = self.get_customer_id(customer_name, customer_email)

        if customer_id is None:
            # Customer doesn't exist, so create a new customer
            customer_id = self.create_customer(customer_name, customer_email)

        if customer_id:
            # Insert a new order into the orders table with the customer_id
            query = "INSERT INTO orders (customer_id, customer_name, customer_email) VALUES (?, ?, ?)"
            params = (customer_id,customer_name, customer_email,)
            order_id = self.db.execute_query(query, params)

            if order_id:
                # Insert meal associations into the order_meals table
                for meal_id in meals:
                    query = "INSERT INTO order_meals (order_id, meal_id) VALUES (?, ?)"
                    params = (order_id, meal_id)
                    self.db.execute_query(query, params)

                return order_id

        return None
    

    def create_customer(self, customer_name, customer_email):
        # Insert customer data into the customers table
        query = "INSERT INTO customers (customer_name, customer_email) VALUES (?, ?)"
        params = (customer_name, customer_email)
        customer_id = self.db.execute_query(query, params)

        if customer_id:
            return customer_id  # Return the ID of the newly created customer
        else:
            return None


    def get_customer_id(self, customer_name, customer_email):
        # Check if the customer already exists based on name and email
        query = "SELECT customer_id FROM customers WHERE customer_name = ? AND customer_email = ?"
        params = (customer_name, customer_email)
        result = self.db.execute_select_query(query, params)

        if result:
            # If a customer with the given name and email exists, return their ID
            return result[0][0]
        else:
            # If no matching customer is found, return None
            return None


    def get_orders(self):
        # Query the database to retrieve orders
        query = """
        SELECT o.order_id, o.customer_name, o.customer_email, o.order_time, o.status_id, o.progress_id
        FROM orders o
        """
        orders = self.db.execute_select_query(query)

        

        formatted_orders = []
        for order in orders:
            # Process and format each order
            query = "SELECT status_name FROM order_statuses WHERE status_id = ?"
            params = (f"{order[4]}")
            status = self.db.execute_select_query(query, params)
            formatted_order = {
                "order_id": order[0],
                "customer_name": order[1],
                "customer_email": order[2],
                "order_time": order[3],      # Include order_time field
                "status_id": status,       # Include status_id field
                "progress_id": order[5],     # Include progress_id field
            }
            formatted_orders.append(formatted_order)

        return formatted_orders

