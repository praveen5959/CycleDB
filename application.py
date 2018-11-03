import sqlite3 as sql
from flask import Flask, render_template,request,session,redirect, url_for
# from flask.ext.session import Session
from datetime import datetime,date,timedelta
import random

app = Flask(__name__)
app.secret_key = '%jsdj!@'

@app.route('/')
def main():
    if 'username' in session:
        return redirect(url_for('index'))

    return redirect(url_for('login'))
@app.route('/login', methods =['GET','POST'])
def login():
    #con = sql.connect('database.db')
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validate = validate_user(username,password)
        if validate == False:
            error = 'Invalid credentials. Please try again'
        else:
            session['username'] = username
            return redirect('/index')
    if 'username' in session:
        return redirect('/index')
    return render_template('login.html',error=error)

def validate_user(username,password):
    con = sql.connect('database.db')
    validate = False
    
    with con:
        cur = con.cursor()
        cur.execute('select user_id, password from customer')
        rows = cur.fetchall()
        for row in rows:
            dUser = row[0]
            dPass = row[1]
            if(dUser == username and dPass == password):
                validate = True
    return validate

@app.route('/signup',methods=['GET','POST'])
def signup():
    con = sql.connect('database.db')
    cur = con.cursor()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        cur.execute('select user_id from customer')
        rows = cur.fetchall()
        for row in rows:
            if(row[0] == username):
                error = 'Username already exist! Try other username'
                return render_template('signup.html',error=error)
        session['username'] = username
        cur.execute("insert into customer values(?,?,?,?)",(username,password,name,email))
        con.commit()
        return redirect('/index')
    if 'username' in session:
        return redirect('/index')
    return render_template('signup.html',error=error)

@app.route('/index')
def index():
    if 'username' in session:
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute('select * from stock')
        rows = cur.fetchall()
        return render_template('index.html',username=session['username'],rows=rows)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



@app.route('/myAccount', methods=['GET'])
def myAccount():
    if 'username' in session:
        username = session['username']
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("select user_id,name,email from customer where user_id = (?)",(username,))
        rows = cur.fetchone()
        #rows has user information, logged in
        print (rows)
        return (rows[0]) #update/change here
    return redirect('/index')

@app.route('/myOrders', methods=['GET'])
def myOrders():
    if 'username' in session:
        username = session['username']
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("select c.name, e.enq_id,e.enq_date, e.cycle_name,g.cat_name,s.sell_price from customer c, enquiry e, category g, stock s where c.user_id = e.user_id and s.cycle_name = e.cycle_name and g.cat_id = e.cat_id and c.user_id = (?)",(username,))
        rows = cur.fetchall()
        return (rows[0][2]) #update/change here
    return redirect('/index')



#---------------------------------------ADMIN PRIORITIES-------------------------------------

@app.route('/addStock',methods = ['GET','POST'])
def addStock():
    con = sql.connect('database.db')
    duplicate = False
    msg = None
    if(request.method == 'POST'):
        cycle_name = request.form['cycle_name']
        cat_id = request.form['cat_id']
        cost_price = request.form['cost_price']
        cycle_image = request.form['image']
        quantity = request.form['quantity']
        duplicate = duplicate_stock(cycle_name)
        if(duplicate == True):
            msg = 'Cycle already in stock'
            return render_template('addStock.html',msg = msg)
        cur = con.cursor()
        cur.execute("insert into stock(cycle_name,cat_id,cost_price,cycle_image,quantity) values(?,?,?,?,?)",(cycle_name,cat_id,cost_price,cycle_image,quantity))
        con.commit()
        msg = "Stock added successfully"
        return render_template('addStock.html',msg=msg)
    return render_template('addStock.html')
def duplicate_stock(cycle_name):

    con = sql.connect('database.db')
    duplicate = False
    
    with con:
        cur = con.cursor()
        cur.execute('select cycle_name from stock')
        rows = cur.fetchall()
        for row in rows:
            dCycle = row[0]
            if(dCycle == cycle_name):
                duplicate = True
                break
    return duplicate



@app.route('/adminLogin', methods=['GET','POST'])
def adminLogin():
    msg = None
    if 'username' in session:
        return redirect('/index')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (username == 'vikash' and password == 'vikash1234'):
            return redirect('/addStock')
        else:
            msg = "Invalid credentials! Try again!"
            return render_template('adminLogin.html',msg=msg)
    return render_template('adminLogin.html')

@app.route('/suppliers')
def suppliers():
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute("select * from suppliers")
    rows = cur.fetchall()
    #rows-> all supplier data

@app.route('/suppliedCycles')
def suppliedCycles():
    #selected_supplier
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute("select p.cycle_name from suppliers s, supplies p where s.s_id = p.s_id and s_id = (?)",(selected_supplier,))
    rows = cur.fetchall()
    #rows->list of cycles by a selected supplier

@app.route('/allRequests')
def allRequests():

    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute("select e.*,c.name,c.email from enquiry e, customer c where c.user_id = e.user_id") 
    rows = cur.fetchall()
    #rows-> shows all the incoming requests from any user

@app.route('/allStock')
def allStock():

    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute("select * from stock") 
    rows = cur.fetchall()
    #rows-> shows all the stocks

if __name__ == "__main__":
    app.run(debug = True)