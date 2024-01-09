from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from flask_socketio import SocketIO, send

from helpers import login_required

import openai

#Configuring application
app = Flask(__name__)

#Configuring session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Allowing application to use the openai and socket libraries
openai.api_key="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"
socketio = SocketIO(app, cors_allowed_origins="*")

#Configuring application to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Subjects page of the website
@app.route("/")
@login_required
def index():
    #Getting all user details based on their session and displaying the page
    school = db.execute('SELECT school FROM users WHERE id = :user_id', user_id=session["user_id"])
    username = db.execute('SELECT username FROM users WHERE id = :user_id', user_id=session["user_id"])
    email = db.execute('SELECT email FROM users WHERE id = :user_id', user_id=session["user_id"])
    return render_template("index.html", username=username, school=school, email=email)

#Subject Choice page of the website
@app.route("/index2", methods=["GET", "POST"])
@login_required
def index2():
    #Getting all user details based on their session and displaying the page
    school = db.execute('SELECT school FROM users WHERE id = :user_id', user_id=session["user_id"])
    username = db.execute('SELECT username FROM users WHERE id = :user_id', user_id=session["user_id"])
    email = db.execute('SELECT email FROM users WHERE id = :user_id', user_id=session["user_id"])
    #Getting the subjects chosen when they submit the form and storing them in the database before displaying the page
    if request.method == "POST":
        subject1 = request.form['lnl']
        level1 = request.form['lnl-l']
        subject2 = request.form['la']
        level2 = request.form['la-l']
        subject3 = request.form['m']
        level3 = request.form['m-l']
        subject4 = request.form['s']
        level4 = request.form['s-l']
        subject5 = request.form['ins']
        level5 = request.form['ins-l']
        subject6 = request.form['ch']
        level6 = request.form['ch-l']
        db.execute("INSERT INTO user_subjects (username, subject1, level1, subject2, level2, subject3, level3, subject4, level4, subject5, level5, subject6, level6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", username[0]["username"], subject1, level1, subject2, level2, subject3, level3, subject4, level4, subject5, level5, subject6, level6)
        subjects = db.execute("SELECT id,subject1, level1, subject2, level2, subject3, level3, subject4, level4, subject5, level5, subject6, level6 FROM user_subjects WHERE username=?", username[0]["username"])
        return render_template("index2.html", username=username, school=school, email=email, subjects=subjects)
    subjects = db.execute("SELECT id,subject1, level1, subject2, level2, subject3, level3, subject4, level4, subject5, level5, subject6, level6 FROM user_subjects WHERE username=?", username[0]["username"])
    return render_template("index2.html", username=username, school=school, email=email, subjects=subjects)

#Subject Reccomendation page of the website
@app.route("/subjectrec", methods=["GET", "POST"])
@login_required
def subjectrec():
    #Getting username based on user session
    username = db.execute('SELECT username FROM users WHERE id = :user_id', user_id=session["user_id"])
    #Taking the text they enter and prompting it to openai(as a career councellor) when they submit the form and displaying the page with the result
    if request.method == "POST":
        messages = []
        messages.append ({"role": "system", "content": "You are a Ib career councellor"})
        question = {}
        question['role'] = 'user'
        question['content'] = request.form['text']+"What subjects can I choose for my IBDP? Give me a 3 possible(and different) 6 subject combinations(3 SL-standard level and 3 HL-higher level always). The IB offers Math-Analysis and approaches, Applications and interpretation; Science-Biology,Chemistry,Computer science,Design technology,Environmental systems and societies,Physics, Sports exercise and health science; Language and Literature A (in any language); Language Aquisition (in any language); Arts-Dance, Film, Music, Theatre, Visual Arts; Individuals and societies- Business management, Digital society, Economics, Geography, Global politics, History, Language and culture, Philosophy, Psychology, Social and cultural anthropology, World religions; 1 math, 1 language and literature, 1 language aquisition, 1 science and 1 humanities are compulsary. The other can be a science, humanity or art.)"

        messages.append(question)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        result = response['choices'][0]['message']['content'].replace('\n', '<br>')
        return render_template("subjectrec.html", username=username, result=result)
    else:
        return render_template("subjectrec.html", username=username)

#Student login page of the website
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    #Forgetting any user_id
    session.clear()

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        teacher = db.execute("SELECT teacher FROM users WHERE username = ?", request.form.get("username"))

        #Ensuring username exists and password is correct
        if not rows:
            flash("Invalid username and/or password")
            return render_template("login.html")
        if not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("login.html")
        #Ensuring they are a student before allowing them to continue
        if teacher[0]["teacher"] == "f":
            session["user_id"] = rows[0]["id"]
        else:
            flash("Please use the teacher login")
            return render_template("login.html")

        #Redirecting user to home page
        return redirect("/")

    else:
        return render_template("login.html")
    
#Teacher login page of the website
@app.route("/logint", methods=["GET", "POST"])
def logint():
    """Log user in"""
    #Forgetting any user_id
    session.clear()

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        teacher = db.execute("SELECT teacher FROM users WHERE username = ?", request.form.get("username"))

        #Ensuring username exists and password is correct and that they are a teacher
        if not rows:
            flash("Invalid username and/or password")
            return render_template("logint.html")
        if not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("logint.html")
        if teacher[0]["teacher"] == "t":
            session["user_id"] = rows[0]["id"]
            subject=db.execute("SELECT subject FROM SISteachers WHERE username = ?", request.form.get("username"))
        else:
            flash("Not a teacher")
            return render_template("logint.html")

        #Redirecting teacher to the chat page of the subject they teach
        return redirect("/t"+subject[0]["subject"]+"t")
    else:
        return render_template("logint.html")

@app.route("/logout")
def logout():
    #Forgetting any user_id
    session.clear()
    # Redirecting user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    #Forgetting any user_id
    session.clear()

    if request.method == "POST":
        #Ensuring passwords meets security requirements(8 digits with numbers)
        passw = request.form.get("password")
        num = 0
        for i in passw:
            if not i.isalpha():
                num += 1
        if len(passw) < 8 or num == 0:
            flash("include atleast 8 digits(including numbers) in your password")
            return render_template("register.html")

        #Ensuring passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            flash("passwords do not match")
            return render_template("register.html")


        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        #Ensuring username doesnt already exist
        if len(rows) != 0:
            flash("username already exists")
            return render_template("register.html")
        
        schooldb= request.form.get("school")+"students"
        student_rows = db.execute(f"SELECT * FROM {schooldb} WHERE username = ?", request.form.get("username"))

        #Ensuring username exists in the list given by the school
        if not student_rows:
            flash("You are not a registered student at "+request.form.get("school"))
            return render_template("login.html")

        #Storing all the data in the users database
        db.execute("INSERT INTO users (username, password, email, school, teacher) VALUES (?,?,?,?, ?)",
                    request.form.get("username"), generate_password_hash(request.form.get("password")), request.form.get("email"), request.form.get("school"),"f")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        #Remembering which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")
    
#Pages for individual subjects
#Chat with students page for AASL
@app.route("/aasl", methods=["GET", "POST"])
@login_required
def aasl():
    @socketio.on('message')
    #Stores messages in the database(messages) and displays the page
    def handle_message (message):
        print("Received message:" + message)
        if message!= "User connected!":
            user_id = session["user_id"]
            db.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", user_id, message)
            send (message, broadcast=True)
    messages = db.execute("SELECT username, message FROM messages JOIN users ON messages.user_id = users.id ORDER BY messages.timestamp")
    username = db.execute('SELECT username FROM users WHERE id = :user_id', user_id=session["user_id"])
    return render_template("aasl.html", username=username, messages=messages)

#Chat between students and teachers for AASL
@app.route("/aaslt", methods=["GET", "POST"])
@login_required
def aaslt():
    @socketio.on('message')
    #Stores messages in the database(messages2) and displays the page
    def handle_message (message):
        print("Received message:" + message)
        if message!= "User connected!":
            user_id = session["user_id"]
            db.execute("INSERT INTO messages2 (user_id, message) VALUES (?, ?)", user_id, message)
            send (message, broadcast=True)
    messages2 = db.execute("SELECT username, message FROM messages2 JOIN users ON messages2.user_id = users.id ORDER BY messages2.timestamp")
    username = db.execute('SELECT username FROM users WHERE id = :user_id', user_id=session["user_id"])
    return render_template("aaslt.html", username=username, messages2=messages2)

#Page for AASL teacher to chat with students
@app.route("/taaslt", methods=["GET", "POST"])
@login_required
def taaslt():
    @socketio.on('message')
    #Stores messages in the database(messages2) and displays the page
    def handle_message (message):
        print("Received message:" + message)
        if message!= "User connected!":
            user_id = session["user_id"]
            db.execute("INSERT INTO messages2 (user_id, message) VALUES (?, ?)", user_id, message)
            send (message, broadcast=True)
    messages2 = db.execute("SELECT username, message FROM messages2 JOIN users ON messages2.user_id = users.id ORDER BY messages2.timestamp")

    #Getting userdetails based on session
    username = db.execute('SELECT username FROM users WHERE id = :user_id', user_id=session["user_id"])
    email = db.execute('SELECT email FROM users WHERE id = :user_id', user_id=session["user_id"])
    school = db.execute('SELECT school FROM users WHERE id = :user_id', user_id=session["user_id"])

    return render_template("taaslt.html", username=username, messages2=messages2, email=email, school=school)

#Resources page for AASL
@app.route("/aaslr", methods=["GET"])
@login_required
def aaslr():
    return render_template("aaslr.html")

#Acts as a replacemnt for pages that arent developed yet
@app.route("/sorry", methods=["GET"])
@login_required
def sorry():
    return render_template("sorry.html")
