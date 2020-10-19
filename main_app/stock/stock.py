from  flask import Flask ,render_template,request,Blueprint,redirect,session
from main_app.app import mydb
from mysql.connector import errors
stock_product=Blueprint('stock',__name__,url_prefix='/stock')


@stock_product.route('/product', methods=['GET']) 
def all_user_func(): 
    if 'user' in session:

        try:
            mycursor = mydb.cursor(dictionary=True)
            sql="SELECT id,product_name,product_price,stock,product_status FROM product "
            mycursor.execute(sql)
            user_details = mycursor.fetchall()

            if user_details == None:
                return 'no user found'
            else:
                print(user_details)
                return render_template('stock/stock.html',  data=user_details)
                    
        except errors.Error as e:
            print("Db error :",e)
            return 'not able to check ,Please try again letter'
    else:
        return redirect('/user/login')