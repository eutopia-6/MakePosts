from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


# reduce unexpected url errors
@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/posts")
def posts():
    return render_template('posts.html')


@app.route("/makePost")
def makePost():
    return render_template('makePost.html')


if __name__ == "__main__":
    app.run(debug=True)

