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
            user='root',
            password='advith@123',
            database='buildit_db'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# API route to handle Sign Up and store in MySQL
@app.route('/signup', methods=['POST'])
def signup():
    # Your existing signup code should be here
    pass  # Remove this line once you add your signup code

# API route to handle Login and authenticate users
@app.route('/login', methods=['POST'])
def login():
    # Get data from the request body
    data = request.get_json()
    
    # Extract the input fields from the JSON
    username = data.get('username')
    password = data.get('password')
    
    # Ensure no fields are missing
    if not all([username, password]):
        return jsonify({"error": "All fields are required!"}), 400
    
    # Database connection
    conn = create_connection()
    
    if conn:
        cursor = conn.cursor()  # Moved cursor initialization here
        try:
            # Check if user exists and password matches
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                return jsonify({"message": "Login successful!", "user_data": {"username": user[1], "reg_no": user[2], "email": user[3]}}), 200
            else:
                return jsonify({"error": "Invalid username or password!"}), 401
            
        except Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        finally:
            cursor.close()  # Ensure cursor is closed if it was created
            conn.close()  # Close the connection
    else:
        return jsonify({"error": "Connection to database failed!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
