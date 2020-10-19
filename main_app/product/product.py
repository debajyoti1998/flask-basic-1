from flask import Flask,render_template,request,Blueprint,session,redirect
from main_app.app import mydb
from mysql.connector import errors

from main_app.helper import __is_alpha_space , __is_number

product_list=Blueprint('product',__name__,url_prefix='/product')



@product_list.route('/add',methods=['GET','POST'])
def product_add_func():
    if "user" in session:
        if request.method== 'POST':
            post_data=request.form
            if __is_alpha_space(post_data['p_name']) and __is_number(post_data['p_price']):
                try:

                    mycursor = mydb.cursor(dictionary=True)
                    sql = "INSERT INTO product (product_name,product_price) VALUES (%s, %s  )"
                    val = (post_data['p_name'], post_data['p_price'] )
                    mycursor.execute(sql, val)
                    mydb.commit()  # mysqlresult = mycursor.fetchall()
                    if (mycursor.rowcount == 1):
                        success_dist = {
                                'message' : 'data saved successfully '
                            }
                        return render_template('product/add_product.html', success=success_dist)
                    else :
                        error_dist = {
                            'message' : 'data not saved , Please try again letter'
                        }
                        return render_template('product/add_product.html', error=error_dist )
                except errors.Error as e:
                    print("Db error :",e)
                    error_dist = {
                        'message' : 'server error , Please try again letter'
                    }
                    return render_template('product/add_product.html', error=error_dist)
            else :
                error_dist = {
                    'message' : 'Please provide proper information'
                }
                return render_template('product/add_product.html', error=error_dist)
        else:
            return render_template('product/add_product.html')
    else:
        return redirect('/user/login')


@product_list.route('/remove')
def remove_func():
    if 'user' in session:
        return 'hello'
    else:
        return redirect('/user/login')
    