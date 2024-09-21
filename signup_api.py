from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection setup
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Update with your MySQL username
            password='advith@123',  # Update with your MySQL password
            database='buildit_db'  # Use your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# API route to handle Sign Up and store in MySQL
@app.route('/signup', methods=['POST'])
def signup():
    # Get data from the request body
    data = request.get_json()
    
    # Extract the input fields from the JSON
    reg_no = data.get('reg_no')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Ensure no fields are missing
    if not all([reg_no, username, email, password]):
        return jsonify({"error": "All fields are required!"}), 400
    
    # Database connection
    conn = create_connection()
    
    if conn:
        try:
            # Insert user data into the 'users' table
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO users (reg_no, username, email, password)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (reg_no, username, email, password))
            conn.commit()  # Commit the transaction
            cursor.close()
            
            return jsonify({"message": "User signed up and stored in the database successfully!"}), 201
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()  # Close the connection
    else:
        return jsonify({"error": "Connection to database failed!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
