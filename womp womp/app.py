from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests
from models import db, User
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aurora.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

tasks = []
speech_text = "Click button to record speech. Say 'stop recording' to stop."
image_link = None  # Store the Google Image link

def get_google_image(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cse_id,
        "key": api_key,
        "searchType": "image",
        "num": 1,  # Number of results to return
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "items" in data:
        return data["items"][0]["link"]  # Return the first image link
    else:
        return "No images found"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            # Update last active time
            user.last_active = datetime.utcnow()
            db.session.commit()
            
            # Redirect teachers to dashboard, students to main page
            if user.is_teacher():
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    global tasks, speech_text, image_link
    
    # Update student's last active time and current task
    if not current_user.is_teacher():
        current_user.last_active = datetime.utcnow()
        current_user.is_active_now = True
        if request.method == 'POST':
            current_user.current_task = f"Working on task: {request.form.get('task', 'Unknown')}"
        db.session.commit()

    if request.method == 'POST':
        if 'add_task' in request.form:
            task = request.form['task'].strip()
            tasks.append({'task': task, 'done': False})
        elif 'mark_done' in request.form:
            index = int(request.form['mark_done'])
            if 0 <= index < len(tasks):
                tasks[index]['done'] = True
        elif 'remove_task' in request.form:
            index = int(request.form['remove_task'])
            if 0 <= index < len(tasks):
                tasks.pop(index)
        elif 'get_image' in request.form:
            speech_text = request.form['get_image'].strip()

            # Query Google Images using the speech text
            api_key = "AIzaSyBE6wcvy8UhNDLks0U907DNGW7LfpEx50U"  # Replace with your actual API key
            cse_id = "c1c4057b1d35f4d99"  # Replace with your Custom Search Engine ID
            image_link = get_google_image(speech_text, api_key, cse_id)

    return render_template('index.html', tasks=tasks, speech_text=speech_text, image_link=image_link)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        teacher_id = request.form.get('teacher_id') if role == 'student' else None

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        user = User(username=username, email=email, role=role)
        if teacher_id:
            user.teacher_id = teacher_id
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('register.html', teachers=teachers)

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_teacher():
        return redirect(url_for('index'))
        
    students = current_user.students
    # Update student active status (inactive after 5 minutes)
    for student in students:
        if student.last_active:
            inactive_time = (datetime.utcnow() - student.last_active).total_seconds()
            student.is_active_now = inactive_time < 300  # 5 minutes
    db.session.commit()
    
    return render_template('teacher_dashboard.html', students=students)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
