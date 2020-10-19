from flask import Flask,render_template,request,Blueprint,session,redirect

# ------ DB--------
from main_app.app import mydb
from mysql.connector import errors

# ------ helper--------
from main_app.helper import __is_alpha_space , __is_email , __create_encryption

# ------ Blueprint--------
user_list=Blueprint('user',__name__,url_prefix='/user')




@user_list.route('/create', methods=['GET','POST']) 
def createuser_func(): 
    
    if request.method == 'POST':
        # ------ save all form data into : post_data variable ------#
        post_data = request.form

        # ------ sanitize user input ------#
        if __is_alpha_space(post_data['name']) and __is_email(post_data['email']) and len(post_data['password']) >4 :
           
            #------ encrypting password --------
            db_pass_to_save = __create_encryption(post_data['password'])
            
            try:

                mycursor = mydb.cursor(dictionary=True)
                sql = "INSERT INTO users (name, email ,password) VALUES (%s, %s , %s )"
                val = (post_data['name'], post_data['email'] ,db_pass_to_save  )
                mycursor.execute(sql, val)
                mydb.commit()  # mysqlresult = mycursor.fetchall()
                if (mycursor.rowcount == 1):
                    success_dist={
                        'message': 'data save successfully'
                    }
                    return render_template('user/create.html',success=success_dist)
                else :
                    error_dist = {
                        'message' : 'data not saved , Please try again letter'
                    }
                    return render_template('user/create.html', error=error_dist )
            except errors.Error as e:
                print("Db error :",e)
                error_dist = {
                    'message' : 'server error , Please try again letter'
                }
                return render_template('user/create.html', error=error_dist)
        else :
            error_dist = {
                'message' : 'Please provide proper information'
            }
            return render_template('user/create.html', error=error_dist)
        
    else :
        return render_template('user/create.html')                                 
    
@user_list.route('/login', methods=['GET','POST'])  
def login_func():
    
    if request.method== 'POST':
        post_data=request.form
        if  __is_email(post_data['email']) and len(post_data['password']) >4 :
            try:
                mycursor = mydb.cursor(dictionary=True)
                sql='SELECT id,name,email,password FROM users WHERE email=%s'
                val=(post_data['email'],)
                mycursor.execute(sql,val)
                user_details = mycursor.fetchone()
                if user_details == None:
                    error_dist = {
                        'message' : 'sorry.. this type of user not found'
                    }
                    return render_template('user/login.html',error=error_dist)
                else:
                    if user_details['password'] ==__create_encryption(post_data['password']):
                        print ( __create_encryption(post_data['password']))
                        session["user"] ={
                            'id' : user_details['id'],
                            'name' : user_details['name'],
                            'email' : user_details['email']
                        } 
                        return redirect('/')
                    else:
                        error_dist = {
                            'message' : 'Error : Email or password mot matched'
                        }
                        return render_template('user/login.html', error=error_dist)
            
            except errors.Error as e:
                print("Db error :",e)
                error_dist = {
                    'message' : 'Error :server error , Please try again letter'
                }
                return render_template('user/login.html', error=error_dist)
        else :
            error_dist = {
                'message' : 'Error : Please provide proper information'
            }
            return render_template('user/login.html', error=error_dist)
    else:
        return render_template('user/login.html')


@user_list.route('/logout', methods=['GET']) 
def user_logout_fun():
    session.pop('user', None)
    return redirect('/user/login')        

 







