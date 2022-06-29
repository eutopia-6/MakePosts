from turtle import up
from flask import Flask, render_template, flash, redirect, request, session, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import base64_encode
from sqlalchemy import TIMESTAMP, func
from io import BytesIO
from PIL import Image
import base64


app = Flask(__name__, template_folder = "../templates", static_folder= "../static")
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MakePosts.db'
app.config["SECRET_KEY"]="secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Upload(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)


@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/makePost", methods = ["GET", "POST"])
def makePost():
    if request.method == "POST":
        file = request.files["file"]
    
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        
        return redirect(url_for('index'))

    return render_template("makePost.html")


@app.route("/posts")
def posts():
    allPosts = Upload.query.all()

    dataList = []
    picList = []
    finalList = []

    for i in range(0, len(allPosts)):
        dataList.append((allPosts[i]).data)

    for x in range(0, len(dataList)):
        picList.append(base64.b64encode(dataList[x]))

    for y in range(0, len(picList)):
        finalList.append((str(picList[y]))[2:-1])

    return render_template("posts.html", Posts = finalList, postNumber = allPosts) 




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
