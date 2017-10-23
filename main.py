from flask import Flask, render_template, request, redirect, flash, session
from app import app, db
from models import Blog, User

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

@app.route("/", methods=["GET", "POST"])
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

# START INSERTED CODE

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usernames = [user.username for user in User.query.all()]
        if username in usernames:
            user = User.query.filter_by(username=username).first()
            if password == user.password:
                session['user'] = user.username
                flash('welcome back, '+user.username)
                return redirect("/")
        flash('bad username or password')
        return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if not username.isalnum():
            flash('zoiks! "' + username + '" does not seem like a valid username!')
            return redirect('/register')
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
            return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/")
    else:
        return render_template('register.html')

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    try:
        del session['user']
    except:
        flash("Not logged in")
    return redirect("/")
    

# END INSERTED CODE


@app.route("/blog", methods=["POST", "GET"])
def blog():
    id = request.args.get("id")
    user = request.args.get("user")
    focus = False
    if id:
        focus = Blog.query.filter_by(id = id)[0]
    if user:
        blogs = Blog.query.filter_by(owner_id=user)
    else:
        blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs, focus=focus)

@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    try:
        if session['user']:
            pass
    except:
        flash("You must login or register before you can post something")
        return redirect("/login")
    if request.method == "POST":
        if request.form["title"] == "" or request.form["body"] == "":
            return redirect("/newpost?error=" + str(True))
        title = request.form["title"]
        body = request.form["body"]
        owner = User.query.filter_by(username = session['user']).first()
        blog = Blog(title,body, owner)
        db.session.add(blog)
        db.session.commit()
        id = blog.id
        return redirect("/blog?id=" + str(id))
    return render_template("newpost.html", error=request.args.get('error'))


if __name__ == "__main__":
    app.run(debug=True)
