from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask_wtf.csrf import CSRFProtect
from flask_login import UserMixin, current_user, login_required, login_user, LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aladinh00-010montext')
csrf = CSRFProtect(app)  

# SQLite Database configuration and integration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuration and setting up of the loginManager library
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirects the user to the login page if not authenticated

# User model database fields
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Task model database fields
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='tasks')

# Initialization and creation of the database
with app.app_context():
    db.create_all()

@login_manager.user_loader  # Loading of the current user in session
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

# Homepage route
@app.route("/homepage")
@login_required
def homepage():
    tasks = Task.query.filter_by(user_id=current_user.id).all()  # Only tasks belonging to the current signed in user to be retrieved
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

        login_user(user)  # Automatic logs in the user to be the current-session user
        flash("Login successful!", "success")
        return redirect(url_for('homepage'))

    return render_template("index.html")

# Add new-task route
@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task_name = request.form.get('task_name')

    if task_name:
        new_task = Task(name=task_name, user_id=current_user.id) 
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('homepage'))

# Task status-update route
@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:  # Only authorized users to update the task status
        flash("Authorization declined!", "danger")
        return redirect(url_for('homepage'))
    
    if task:
        task.status = request.form['status']

        db.session.commit()
        flash("Task status updated successfully!", "success")
    else:
        flash("Task not found!", "danger")
    return redirect(url_for('homepage')) 

# Task name-update route
@app.route('/update_task_name/<int:task_id>', methods=['PUT'])
def update_task_name(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:  # Only authorized users to update the task name
        flash("Authorization declined!", "danger")
        return redirect(url_for('homepage'))
    
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    new_name = data.get('name', '').strip()

    if not new_name:
        return jsonify({"error": "Task name cannot be empty"}), 400

    task.name = new_name
    db.session.commit()
    flash("Task updated successfully!", "success")

    return redirect(url_for('homepage'))

# Task deletion route
@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:  # Only authorized users to delete the task
        flash("Authorization declined!", "danger")
        return redirect(url_for('homepage'))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    
    return redirect(url_for('homepage'))

if __name__ == "__main__":
    app.run(debug=True)
