from flask import Flask,render_template,request,redirect,session

import mysql.connector
from mysql.connector import errors

try:
    mydb = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='instagram')
    if mydb.is_connected():
        print ('database connected')
    else:
        print ('database not connected')    
except errors.Error as e:
    print("Db error :",e)      





app=Flask(__name__) 
app.secret_key = "babun1234__sec"


#------------users route-----------------
from main_app.user.user import user_list
app.register_blueprint(user_list)


#------------product-----------------
from main_app.product.product import product_list
app.register_blueprint(product_list)


#------------transaction---------------------
from main_app.transaction.transaction import transaction_list
app.register_blueprint(transaction_list)


#------------------stock------------------
from main_app.stock.stock import stock_product
app.register_blueprint(stock_product)


@app.route('/')
def app_route():
    if "user" in session:
        return render_template('index.html')
    else:
        return redirect('/user/login')

