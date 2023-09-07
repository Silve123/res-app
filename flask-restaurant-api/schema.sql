-- Create the customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_email TEXT
);

-- Create the progress table
CREATE TABLE IF NOT EXISTS progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    progress_status TEXT NOT NULL
);

-- Create the order_statuses table
CREATE TABLE IF NOT EXISTS order_statuses (
    status_id INTEGER PRIMARY KEY,
    status_name TEXT NOT NULL UNIQUE
);


-- Create the meals table with description and price columns
CREATE TABLE IF NOT EXISTS meals (
    meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_name TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    description TEXT,
    price REAL
);


CREATE TABLE IF NOT EXISTS order_meals (
    order_id INTEGER,
    meal_id INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
);


-- Create the orders table with a default status_id
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    customer_name TEXT NOT NULL,
    customer_email TEXT,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_id INTEGER DEFAULT 1,  -- Set a default value
    progress_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (progress_id) REFERENCES progress(progress_id),
    FOREIGN KEY (status_id) REFERENCES order_statuses(status_id)
);




