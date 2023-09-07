import sqlite3


def create_sqlite_tables(database_name, sql_filename):
    conn = None
    try:
        # Connect to SQLite database or create it if it doesn't exist
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Read and execute the SQL script
        with open(sql_filename, 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)

        # Commit changes
        conn.commit()
        print("SQLite tables created successfully!")

        # Populate the progress, meals, and order_statuses tables
        populate_tables(conn)
        print("Tables populated with data!")

    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")

    finally:
        if conn is not None:
            conn.close()


def populate_tables(conn):
    try:
        cursor = conn.cursor()

        # Populate the progress table (unchanged)
        cursor.executescript("""
        INSERT INTO progress (progress_status) VALUES
        ('in_kitchen'),
        ('started'),
        ('complete'),
        ('out_kitchen');
        """)

        # Populate the meals table with description and price (modified)
        cursor.executescript("""
            INSERT INTO meals (meal_name, meal_type, description, price) VALUES
            ('Burger', 'meal', 'Delicious burger with lettuce and cheese', 8.99),
            ('Pizza', 'meal', 'Classic pepperoni pizza', 10.99),
            ('Coke', 'drink', 'Refreshing Coca-Cola', 2.49),
            ('Water', 'drink', 'Bottled water', 1.99);
        """)


        # Populate the order_statuses table
        cursor.executescript("""
        INSERT INTO order_statuses (status_name) VALUES
        ('infant'),
        ('adult'),
        ('retirement');
        """)

        # Commit changes
        conn.commit()

    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")




if __name__ == "__main__":
    # SQLite database name
    database_name = 'orders.db'

    # Path to your SQL file
    sql_filename = 'schema.sql'

    # Create SQLite tables and populate them
    create_sqlite_tables(database_name, sql_filename)
