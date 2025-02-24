from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error  # Make sure this is imported


app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'db',  # Changed to '127.0.0.1' instead of 'localhost'
    'user': 'root',  # your MySQL username
    'password': 'FatiMa@2003',  # your MySQL password
    'database': 'library_db',
    'port': 3306,
    'connection_timeout': 10 
}

# Connect to MySQL
# Function to get database connection
def get_db_connection():
    try:
        #pdb.set_trace()
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the database.")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


@app.route('/')
def index():
    # Connect to database and fetch all books
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        

        # Connect to database and insert the new book
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/delete/<int:id>')
def delete_book(id):
    # Connect to database and delete the book by ID
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True) 
