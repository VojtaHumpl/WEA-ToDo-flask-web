from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__, template_folder=".")

@app.route('/')
def home():
    return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return "yeet" #redirect(url_for('home'))
    return render_template('login.html', error=error)





    