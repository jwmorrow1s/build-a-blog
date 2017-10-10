from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pass@localhost:3306/build_a_blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body




@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/blog", methods=["POST", "GET"])
def blog():
    id = request.args.get("id")
    focus = False
    if id:
        focus = Blog.query.filter_by(id = id)[0]

    blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs, focus=focus)

@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    if request.method == "POST":
        if request.form["title"] == "" or request.form["body"] == "":
            return redirect("/newpost?error=" + str(True))
        title = request.form["title"]
        body = request.form["body"]
        db.session.add(Blog(title,body))
        db.session.commit()
        id = db.engine.execute("SELECT MAX(id) from blog;").fetchone()[0]
        return redirect("/blog?id=" + str(id))
    return render_template("newpost.html", error=request.args.get('error'))


if __name__ == "__main__":
    app.run(debug=True)
