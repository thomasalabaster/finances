from array import array
from cgi import test
import re
from flask import Flask, flash, redirect, render_template, request, session
import os
import psycopg2
from psycopg2 import Error
from datetime import timedelta

app = Flask(__name__)

# Set secret key and logout timer
app.secret_key = "test"
app.permanent_session_lifetime = timedelta(hours=1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif "username" in session:
        return redirect("/user")
    else:
        # Obtain entered username and password
        username = request.form.get("username")
        password = request.form.get("password")
        session['username'] = username

        # Obtain connection and cursors for SQL Querying
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query db to see if username exists
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        temp = cursor.fetchall()
        if len(temp) < 1:
            return render_template("error.html")

        # Check password
        # Needs hashing in the future
        actual_password = temp[0][1]
        if password != actual_password:
            return render_template("error.html")
        return redirect('/user')
        return render_template("error.html")

@app.route("/user")
def user():
    # Check if there is a current user logged in
    if "username" in session: 
        username = session['username']
        
        # Get transactions and current bank balance

        # Obtain connection and cursors for SQL Querying
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        id = cursor.fetchall()
        id = id[0]
        cursor.execute("SELECT bank_balance FROM transactions WHERE user_id = %s", (id,))
        transactions = cursor.fetchall()[0][0]
        print(transactions)

        return render_template("user.html", username=username, transactions=transactions)
    else:
        return redirect("/login")

@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # Obtain username and passwords
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        surname = request.form.get("surname")
        confirmation = request.form.get("confirmation")

        # Obtain connection and cursors for SQL Querying
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if form filled out correctly (e.g. empty or not matching passwords)
        if not username:
            return render_template("error.html")
        if not password or not confirmation:
            return render_template("error.html")
        if password != confirmation:
            return render_template("error.html")
        if not first_name or not surname:
            return render_template("error.html")

        # Check if user already exists, convert the variable to tuple
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        temp = cursor.fetchall()
        if len(temp) == 1:
            return render_template("error.html")

        # Insert new user into SQL db
        temp_args = (username, password, first_name, surname)
        temp_execute = """
                        INSERT INTO users (username, password, first_name,
                        last_name) VALUES (%s, %s, %s, %s)
                        """
        cursor.execute(temp_execute, temp_args)

        # Close SQL connection
        connection.commit()
        connection.close()
 
        # Registration successful, redirect to login page
        return render_template("login.html")

@app.route("/logout") 
def logout():
    session.pop("username")
    return render_template("login.html")
    
def get_db_connection():
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                password="Otelfingen",
                                host="localhost",
                                port="5432",
                                database="finance")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    return connection

    