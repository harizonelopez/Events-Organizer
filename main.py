from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aladinh00-010montext')

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')

# Initialize database
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

# User registration route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required!", "error")
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("User registered successfully!", "success")
        return redirect(url_for('login'))

    return render_template("index.html")

# User login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password!", "error")
            return redirect(url_for('login'))

        flash("Login successful!", "success")
        return redirect(url_for('tasks'))

    return render_template("index.html")

# Tasks route
@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        task_name = request.form.get("task_name")
        if task_name:
            new_task = Task(name=task_name)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
            return redirect(url_for('tasks'))

    tasks = Task.query.all()
    return render_template("home_page.html", tasks=tasks)

# Task deletion route
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted!", "success")
    return redirect(url_for('tasks'))

if __name__ == "__main__":
    app.run(debug=True)
