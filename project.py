from flask import Flask, redirect, request, session, url_for, render_template
from models import User, db

app = Flask(__name__)
app.secret_key = "Super duper secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"


db.init_app(app)

@app.cli.command('initdb')
def db_init():
    with app.app_context():
        db.create_all()

@app.route("/")
def default():
    return redirect(url_for("login_controller"))

#query to authenticate users
def authenticate_user(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user

#login page
@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if  "username" in session:
        return redirect(url_for("profile", username=session["username"]))
    elif request.method == "POST":
        username = request.form["user"]
        password = request.form["pass"]
        user = authenticate_user(username, password)
        if user:
            session["username"] = username
            session["id"] = user.id
            return redirect(url_for("profile", username=username))

    return render_template("login_scrn.html")

#for users to create account
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        acc_username = request.form.get("username")
        acc_password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        user = User(username=acc_username, password=acc_password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login_controller"))
    
    return render_template("create_acc.html")

#for user profile
@app.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("profile.html", user=user)
    else:
        return "User not found"
    
#logout
@app.route("/logout/")
def logout():
    if "username" in session:
        session.clear()
        return render_template("logout_scrn.html")
    else:
        return redirect(url_for("login_controller"))