from flask import Flask,render_template,request,Blueprint,session,redirect
from main_app.app import mydb
from mysql.connector import errors

from main_app.helper import __is_number , __is_alpha_space,__is_number

transaction_list=Blueprint('transaction',__name__,url_prefix='/transaction')

@transaction_list.route('/sell', methods=['GET','POST'])
def tranction_func():
    if "user" in session:
        if request.method=='POST':
            post_data=request.form
            if __is_number(post_data['product_id']) and __is_alpha_space(post_data['costomar']) and __is_number(post_data['amount']):
                try:
                    mycursor = mydb.cursor(dictionary=True)
                    sql='INSERT INTO txn (product_id,amount,customer) VALUES (%s,%s,%s)'
                    val=(post_data['product_id'],post_data['amount'],post_data['costomar'])
                    mycursor.execute(sql,val)
                    mydb.commit()
                    if (mycursor.rowcount==1):
                        sql='UPDATE  product SET stock = stock- %s WHERE id = %s '
                        val=(post_data['amount'],post_data['product_id'])
                        mycursor.execute(sql,val)
                        mydb.commit()
                        if (mycursor.rowcount==1):
                            success_dist = {
                                'message' : 'data saved successfully '
                            }
                            return render_template('trxn/purches.html', success=success_dist)
                        else:
                            return "all not ok"
                    else:
                        error_dist = {
                        'message' : 'data not save ... please try again'
                        }
                        return render_template('trxn/sell.html', error=error_dist)

                except errors.Error as e:
                    print("Db error :",e)
                    error_dist = {
                        'message' : 'server error , Please try again letter'
                    }
                    return render_template('trxn/sell.html', error=error_dist)

            else :
                error_dist = {
                    'message' : 'Please provide proper information'
                }
                return render_template('trxn/sell.html', error=error_dist)
        else:
            return render_template('trxn/sell.html')
    else:
        return redirect('/user/login')


@transaction_list.route('/purches',methods=['GET','POST'])
def purches_func():
    if 'user' in session:
        if request.method=='POST':
            post_data=request.form
            if __is_number(post_data['product_id']) and __is_alpha_space(post_data['vendor']) and __is_number(post_data['amount']):
                try:
                    mycursor = mydb.cursor(dictionary=True)
                    
                    
                    sql='INSERT INTO txn (product_id,amount,vendor) VALUES (%s,%s,%s)'
                    val=(post_data['product_id'],post_data['amount'],post_data['vendor'])
                    mycursor.execute(sql,val)
                    mydb.commit()
                    if (mycursor.rowcount==1):
                        sql='UPDATE  product SET stock = stock+ %s WHERE id = %s '
                        val=(post_data['amount'],post_data['product_id'])
                        mycursor.execute(sql,val)
                        mydb.commit()
                        if (mycursor.rowcount==1):
                            success_dist = {
                                'message' : 'data saved successfully '
                            }
                            return render_template('trxn/purches.html', success=success_dist)
                        else:
                            return "all not ok"
                    else:
                        error_dist = {
                            'message' : 'data not save ... please try again'
                        }
                        return render_template('trxn/purches.html', error=error_dist)
               
                except errors.Error as e:
                    print("Db error :",e)
                    error_dist = {
                        'message' : 'server error , Please try again letter'
                    }
                    return render_template('trxn/purches.html', error=error_dist)

            else :
                error_dist = {
                    'message' : 'Please provide proper information'
                }
                return render_template('trxn/purches.html', error=error_dist)
        else:
            return render_template('trxn/purches.html')
    else:
        return redirect('/user/login')




