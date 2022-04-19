from flask import Flask, flash, redirect, render_template, request, session




# Configure application
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"
