from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'HIII'


@app.route('/')
def home():
   return render_template('retail.html')


@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/signin')
def signin():
   return render_template('signin.html')

@app.route('/signup')
def signup():
   return render_template('signup.html')

'''@app.route('/list')
def list():
   return render_template('list.html')'''



@app.route('/data',methods = ['POST', 'GET'])
def data():
   if request.method == 'POST':
      try:
         username = request.form['username']
         email = request.form['email']
         password = request.form['password']
          
         
         with sql.connect("student_database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (username,email,password) VALUES (?,?,?)",(username,email,password) )
            con.commit()
            msg = "Record successfully added!"
      except:
         con.rollback()
         msg = "error in insert operation" 
      
      finally:
        return render_template("list.html",msg = msg)
        con.close()     

@app.route('/list')
def list():
   con = sql.connect("student_database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   students = cur.fetchall()
   return render_template("list.html", students = students)

if __name__ == '__main__':
   app.run(debug = True)


'''@app.route('/siginpage')
def signinpage():
   return render_template('signinpage.html')'''
