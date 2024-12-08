from flask import Flask, render_template, request, redirect, url_for, session, flash
from extensions import db
from models import User, Todo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)

# Initialize extensions
db.init_app(app)

# Routes and Logic
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Correct method
    print(f"Signup attempt: Email={email}, HashedPassword={hashed_password}")
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("User already exists. Please login.")
        return redirect(url_for('index'))

    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash("Signup successful! Please login.")
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    todos = Todo.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', todos=todos)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    content = request.form['content']
    new_todo = Todo(content=content, user_id=session['user_id'])
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/update_todo/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        todo.content = request.form['content']
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))

# App Initialization
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
