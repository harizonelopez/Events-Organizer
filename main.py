from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aladinh00-010montext')
csrf = CSRFProtect(app)  

# SQLite database configuration and integration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
def index():
    return render_template("index.html")

# Homepage route
@app.route("/homepage")
def homepage():
    tasks = Task.query.all()
    return render_template("home_page.html", tasks=tasks)  

# User registration route
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if not username or not password or not confirm_password:
        flash("All fields are required!", "error")
        return redirect(url_for("index"))

    if password != confirm_password:
        flash("Passwords do not match!", "error")
        return redirect(url_for("index"))

    if User.query.filter_by(username=username).first():
        flash("Username already exists!", "error")
        return redirect(url_for("index"))  
                
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("User registered successfully!", "success")
    return redirect(url_for('login'))           

    # return render_template("index.html")

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

        session['user_id'] = user.id
        flash("Login successful!", "success")
        return redirect(url_for('homepage'))

    return render_template("index.html")

# Add new task route
@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')

    if task_name:
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('homepage'))

# Task status update route
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        flash("Task not found!", "error")
        # return jsonify({"error": "Task not found"}), 404

    task.status = request.json.get('status', task.status)
    db.session.commit()
    
    flash("Task updated successfully!", "success")
    # return jsonify({"message": "Task updated successfully"}), 200

# Task deletion route
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        flash("Task not found!", "error")
        # return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    
    flash("Task deleted successfully!", "success")
    # return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
