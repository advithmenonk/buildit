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

# API route to handle stopwatch data and store in MySQL
@app.route('/stopwatch', methods=['POST'])
def stopwatch():
    # Get data from the request body
    data = request.get_json()
    
    # Extract the study duration and topic
    study_duration = data.get('study_duration')
    topic = data.get('topic')
    
    # Ensure study duration is provided
    if not study_duration:
        return jsonify({"error": "Study duration is required!"}), 400
    
    # Database connection
    conn = create_connection()
    
    if conn:
        try:
            # Insert stopwatch data into the 'sessions' table
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO sessions (study_duration, topic)
                VALUES (%s, %s)
            """
            cursor.execute(insert_query, (study_duration, topic))
            conn.commit()  # Commit the transaction
            cursor.close()
            
            return jsonify({"message": "Stopwatch data stored in the database successfully!"}), 201
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()  # Close the connection
    else:
        return jsonify({"error": "Connection to database failed!"}), 500

if __name__ == '__main__':
    app.run(debug=True)