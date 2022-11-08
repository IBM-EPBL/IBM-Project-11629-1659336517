from flask import Flask,render_template, flash,redirect, url_for,request
app = Flask(__name__)
app.secret_key="hello"

@app.route("/")
def index():
	return render_template("index.html")
	



@app.route("/about")                                      
def about():
	return render_template("about.html")


@app.route("/list")
def list():
   return render_template("list.html")


@app.route('/signin',methods=["post","get"])
def signin():
  return render_template('signin.html')


@app.route('/signup',methods=["post","get"])
def signup():
  return render_template('signup.html')
