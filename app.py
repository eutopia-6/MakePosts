from flask import Flask, render_template, flash, redirect, request, session, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, func
from io import BytesIO

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SECRET_KEY'] = "b'\x00\xb4\x8d\xbe\xf8\xa3\x1e;l\xf4,\x12'"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MakePosts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# init blog database
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeCreated = db.Column(TIMESTAMP, nullable=False, server_default=func.now())
    title = db.Column(db.String(), unique=False, nullable=False)
    content = db.Column(db.String(), unique=False, nullable=False)
    fileName = db.Column(db.String())
    fileData = db.Column(db.LargeBinary)


# reduce unexpected url errors
@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])


# index page, view all blog posts
@app.route("/")
def index():
    allPosts = Posts.query.all()
    allPosts.reverse()


    return render_template('index.html', posts=allPosts)


@app.route("/database")
def database():
    allPosts = Posts.query.all()

    return render_template('fileDataBase.html', posts=allPosts)


# view a blog post
@app.route("/<int:post_id>")
def posts(post_id):
    postID = Posts.query.filter_by(id=post_id).first()

    return render_template('posts.html', post=postID)


# display the file of a blog post
@app.route("/<int:post_id>/display")
def display(post_id):
    postID = Posts.query.filter_by(id=post_id).first()

    return send_file(BytesIO(postID.fileData), download_name=postID.fileName)


# download a post's file
@app.route("/<int:post_id>/download")
def download(post_id):
    postID = Posts.query.filter_by(id=post_id).first()

    return send_file(BytesIO(postID.fileData), attachment_filename=postID.fileName, as_attachment=True)


# create a blog post
@app.route("/createPost", methods=('GET', 'POST'))
def createPost():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']

        if not title:
            flash('Title is required!')
        else:
            new_post = Posts(title=title, content=content, fileName=file.filename, fileData=file.read())
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('createPost.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
