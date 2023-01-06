from flask import Blueprint, redirect, render_template, request, session, jsonify
from flask_login import login_required, login_user, logout_user
from User import User
from sanitizer import sanitize
from bson import ObjectId
import hashlib
from . import login_manager, logins, tasks


main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id: str):
    """
    User loader, needed for flask_login to work with the current user

    Args:
        user_id (str): User id

    Returns:
        User with the corresponding user_id, else None
    """
    id = session.get("curr_user")
    if id == user_id:
        #verifiy user exists in database
        res = logins.find_one({"name": user_id})
        if res is None:
            return None
        user = User(user_id)
        user.is_authenticated = True
        return user
    return None

@main.route('/')
def init():
    """
    Default redirect to login
    """
    return redirect('/login')

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page

    Returns:
        if valid login -> redirect to home page
        else -> return nothing
    """
    if request.method == 'POST':

        #sanitize input first
        username = sanitize(request.form['username'])
        #password doesn!t need to get sanitized, because of sha256 hashing
        password = hashlib.sha256(request.form['password'].encode("utf-8")).hexdigest()

        # find user in database
        res = logins.find_one({"name": username})
        
        #verify user login
        if res is not None and res["password"] == password:
            user = User(res["name"])
            login_user(user, remember=False)
            #save current user
            session["curr_user"] = user.get_id()
        else:
            return

        return redirect("/home")

    return render_template('login.html')

@main.route("/logout")
@login_required
def logout():
    """
    User logout, clears session

    Returns:
        redirect to login page
    """
    logout_user()
    session.clear()
    return redirect("/login")

@main.route("/home")
@login_required
def home():
    """
    Home page with user's tasks

    Returns:
        Rendered index.html
    """
    return render_template("index.html", userTasks=getTasks())

@main.route("/addTask")
@login_required
def addTask():
    """
    Adds new task to database for current user

    Returns:
        Rendered index.html
    """
    status = request.args.get("status")
    content = request.args.get("content")
    tasks.insert_one({"user": session["curr_user"], "status": status, "content": content})
    return render_template("index.html", userTasks=getTasks())

@main.route("/removeTask")
@login_required
def removeTask():
    """
    Removes a task from database for current user

    Returns:
        Rendered index.html
    """
    id = request.args.get("id")
    tasks.delete_one({"_id": ObjectId(id)})
    return render_template("index.html", userTasks=getTasks())

@main.route("/updateTask")
@login_required
def updateTask():
    """
    Updates a task in database for current user

    Returns:
        Rendered index.html
    """
    id = request.args.get("id")
    status = request.args.get("status")
    content = request.args.get("content")

    if content is not None:
        tasks.update_one({"_id": ObjectId(id)}, {"$set": {"status": status, "content": content}})
    else:
        tasks.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})

    return render_template("index.html", userTasks=getTasks())

@main.route("/json")
@login_required
def jsonFormat():
    """
    Generates json from tasks in database for current user

    Returns:
        user's tasks in json format
    """
    return jsonify(getTasks())

def getTasks():
    """
    Returns all tasks from the database for current user
    """
    res = tasks.find({"user": session["curr_user"]})
    userTasks = []
    for task in res:
        userTasks.append({"id": str(task["_id"]), "status": task["status"], "content": task["content"]})
    return userTasks
