from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from re import match
from datetime import datetime


app = Flask(__name__)

app.secret_key ='hello'

# Remote MySQL Configuration

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12577529'
app.config['MYSQL_PASSWORD'] = 'zQawPfchIJ'
app.config['MYSQL_DB'] = 'sql12577529'


mysql = MySQL(app)

# Stock Notification


def notify_stock():
    # This function sends you a notification of stock shortage
    print('***********Running Notify**************')
    if 'username' in session:
        print('***********Executing Notify************')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM shop;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()

        

        """ for item in items:
            if item[4] < item[6]:
                message = f'Hi, Your stock {item[1]} with Iventory ID {item[0]} is below the reoder level. Please refill it as soon as possible to ignore the shortage of product in your shop.'
                sendmail(subject, message, to_mail)
                print('Mail has been sent.')
    else:
        print('*********Session is Empty**********')"""

# ************************Rendering Pages***********************


@app.route('/')
def index():
    # A route to home page
    notify_stock()
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # A page where anyone can contact the IMS admin
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        date = datetime.now()

        # Validating Data
        if len(name) < 3:
            msg = 'Length of name must be grater than 2 characters.'
            return render_template('contact.html', msg=msg)
        elif len(subject) < 10:
            msg = 'Subject must be grater than 10 characters'
            return render_template('contact.html', msg=msg)
        elif len(message) < 10:
            msg = 'Message must be grater than 10 characters'
            return render_template('contact.html', msg=msg)
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO contacts (name, email, subject, messsage, date) VALUES (%s, %s, %s, %s, %s)',
                           (name, email, subject, message, date))
            mysql.connection.commit()
            cursor.close()
            msg = 'We have successfully received your request.'
            #sendmail('IMS ContactUs', 'We have successfully received your request. We\'ll be touch in with you soon.', email)
            return render_template('index.html', msg=msg)

    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # A function to register new users
    msg = None
    data = None
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        mail = request.form['mail']
        contact = request.form['contact']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        check = request.form.get('t&c')
        
        # Check if user already exists
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = f'User with username {username} already exists. Please select another username.'
            return render_template('register.html', msg=msg, valid=False)
        
        if check == 'on':
            check = True
        else:
            check = False

        # Validation of data
        if len(name) < 3:
            msg = 'Name must be greater than 2 characters'
            return render_template('register.html', msg=msg, valid=False)

        if len(username) < 8:
            msg = 'Username must be greater than 8 chars'
            return render_template('register.html', msg=msg, valid=False)

        regex = "^(?=.{8, 20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
        if match(regex, username):
            msg = 'Only aA-Zz, 0-9, _ . allowed.'
            return render_template('register.html', msg=msg, valid=False)

        if len(password) < 8:
            msg = 'Password must be at least 8 characters long'
            return render_template('register.html', msg=msg,  valid=False)
        if password != confirmPassword:
            msg = 'Alert! Password Mismatch'
            return render_template('register.html', msg=msg,  valid=False)
        elif not check:
            msg = 'You must agree all T&Cs.'
            return render_template('register.html', msg=msg, check=check, valid=True)

        data = [username, name, mail, contact, password, check]

        # Storing data to database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users(username, name, email, contact, password, agree) VALUES(%s, %s, %s, %s, %s, %s )',
                       (username, name, mail, contact, password, check))
        mysql.connection.commit()
        cursor.close()

        msg = 'Successfully Registered'

        #sendmail('IMS Sinup Info', 'You are successfuly registered in IMS. Your username is {} and your password is {}. Please do not share with anyone.'.format( username, password), mail)

        return render_template('login.html', msg=msg)
    return render_template('register.html', success_msg=msg, msg=msg, valid=True, check=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Managing Authentication
    user_data = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username, password, email from users where username = %s', (username,))
        mysql.connection.commit()
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            if password == user_data[1]:
                session['username'] = username
                session['email'] = user_data[2]

                # sending email
                message = f'{username}, You have successfully logged into IMS on {datetime.now()}. If this is not you then send us a message at 9876543210 with your username from registered number.'
                to_mail = user_data[2]
                #sendmail('IMS Security Review', message, to_mail)
                msg = 'You are successfully logged in!'
                notify_stock()
                return render_template('index.html', session=session, msg=msg)

            else:
                msg = 'Password do not match'
                return render_template('login.html', msg=msg)

        else:
            msg = 'Sorry ! No such user exists.'
            return render_template('login.html', msg=msg)

    else:
        if 'username' in session:

            message = f'{session[username]}, You have successfully logged into IMS on {datetime.now()}. If this is not you then send  us at 9876543210 with your username from registered number.'
            to_mail = session.get('email')
            #sendmail('IMS Security Review', message, to_mail)
            notify_stock()

            return redirect(url_for('index'))

    return render_template('login.html', user_data=user_data)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# ***********************Managing services*****************************

@app.route('/services')
def services():
    # This function shows the IMS Table shop items
    if 'username' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM shop;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()
        notify_stock()
        return render_template('ims.html', items=items)

    msg = 'Please! login first to use IMS services.'
    return render_template('login.html', msg=msg)


@app.route('/update')
def details():
    # This function simply throws you on update and delete page
    if 'username' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM shop;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()
        notify_stock()
        return render_template('update.html', items=items)
    return render_template('login.html')


# update delete add products

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    # This function set id in input box of delete page
    id = id
    if 'username' in session:
        notify_stock()
        return render_template('deleteitem.html', id=id)
    else:
        msg = "You must login to delete."
        return render_template('login.html', msg=msg)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    # This function perform the delete operation
    if 'username' in session:
        if request.method == 'POST':
            iid = request.form['iid']
            cursor = mysql.connection.cursor()
            cursor.execute('DELETE FROM shop where iid = %s', (iid,))
            mysql.connection.commit()
            cursor.close()
            msg = "You have successfully deleted the item."

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM shop;')
            mysql.connection.commit()
            items = cursor.fetchall()
            cursor.close()
            notify_stock()
            return render_template('update.html', msg=msg, items=items)


@app.route('/add', methods=['GET', 'POST'])
def add():
    # This function add a new product to shop
    msg = ""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['desc']
        price = request.form['price']
        stock = request.form['stock']
        reorder_level = request.form['reol']
        total = int(price) * int(stock)

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO shop(name, description, price, stock, total, reorder_level) VALUES(%s, %s, %s, %s, %s, %s )',
                       (name, description, price, stock, total, reorder_level))

        mysql.connection.commit()
        cursor.close()
        msg = 'New product successfully added!'
        notify_stock()

    return render_template('additem.html', msg=msg)


@app.route('/updateitem/<int:id>')
def updateitem(id):
    # This function set the previous values in input box on update page
    id = id
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM shop WHERE iid=%s', (id,))
    mysql.connection.commit()
    data = cursor.fetchone()
    cursor.close()
    mydata = {'id': data[0], 'name': data[1], 'desc': data[2], 'price': data[3],
              'stock': data[4], 'total': data[5], 'reorder': data[6]}
    notify_stock()
    return render_template('updateitem.html', data=mydata)


@app.route('/updateprod', methods=['GET', 'POST'])
def update():
    # This function perform the update
    if request.method == 'POST':
        id = request.form['iid']
        name = request.form['name']
        description = request.form['desc']
        price = request.form['price']
        stock = request.form['stock']
        reorder_level = request.form['reol']
        total = int(price) * int(stock)

        cursor = mysql.connection.cursor()
        cursor.execute('Update shop SET name=%s, description=%s, price=%s, stock=%s, total=%s, reorder_level=%s WHERE iid=%s',
                       (name, description, price, stock, total, reorder_level, id))

        mysql.connection.commit()
        cursor.close()
        msg = 'Successfully updated!'

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM shop;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()
        notify_stock()
        return render_template('update.html', msg=msg, items=items)


@app.route('/billing', methods=['GET', 'POST'])
def billing():
    # Creating a billing system
    iid = None
    if 'username' in session:
        if request.method == 'POST':
            iid = request.form.get('iid')
            if iid:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM shop WHERE iid=%s', (iid,))
                mysql.connection.commit()
                items = cursor.fetchall()
                cursor.close()
                notify_stock()
                return render_template('billing.html', items=items)
            else:
                msg = 'Please enter a valid product id'
                return render_template('billing.html', msg=msg)
                notify_stock()

        notify_stock()
        return render_template('billing.html')


@app.route('/forgetpass', methods=['GET', 'POST'])
def forgetpass():
    if request.method == 'POST':
        username = request.form['username']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username, password, email from users where username = %s', (username,))
        mysql.connection.commit()
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            password = user_data[1]
            mail = user_data[2]
            message = f'Hello {username}, Your password is {password}. Please delete this mail after getting it back for your security. Thank you!'
            #sendmail('IMS PASSWORD INFO', message, mail)
            print("************Password Sent on Mail Successfully************")
            msg = 'Password sent on registered mail successfully'
            return render_template('login.html', msg=msg)
        else:
            msg = 'No such user exists!'
            return render_template('passwordforget.html', my_msg=msg)
            
    return render_template('passwordforget.html',my_msg='')


@app.route('/updatepass', methods=['GET', 'POST'])
def updatepass():
    if request.method == 'POST':
        uname = request.form['username']
        oldpass = request.form['password']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']

        if pass1 != pass2:
            msg = 'New password not matched!'
            return render_template('passwordupdate.html', my_msg=msg)

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username, password, email from users where username = %s', (uname,))
        mysql.connection.commit()
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            if oldpass == user_data[1]:
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE `users` SET `password`=%s WHERE `username`=%s', (uname, pass1))
                mysql.connection.commit()
                cursor.close()
                msg = 'Password updated successfully'
                print('************password updated successfully****************')
                return render_template('login.html', msg=msg)
        else:
            msg = 'Username or Password is Incorrect'
            return render_template('passwordupdate.html', my_msg=msg)
    return render_template('passwordupdate.html', my_msg='')
        
        
# Running flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
