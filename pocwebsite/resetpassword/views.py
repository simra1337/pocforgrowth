from distutils.log import error
import sys
from django.shortcuts import render
import mysql.connector as sql
import os
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


# Create your views here.

cpass = ''
password= ''

@csrf_exempt
def resetPasswordAction(request, token):
    global password, cpass
    try:
        if request.method == 'POST':
            m=sql.connect(host=os.getenv('HOST', default='localhost'), user=os.getenv('DBUSER'), passwd=os.getenv('PASSWORD'), database = os.getenv('DATABASE'))
            cursor = m.cursor()
            d = request.POST
            error_message=''
            for key,value in d.items():
                if key == "password":
                    if not value:
                        error_message = "Password required"
                    elif len(value) < 6:
                        error_message = "Password length should be more than 6"
                    else:
                        password = value
                if key == "cpassword":
                    if not value:
                        error_message = "Confirm Password Required"
                    elif len(value) < 6:
                        error_message = "Password length should be more than 6"
                    elif password!=value:
                        error_message = "Both password should be same"
                    else:
                        cpass = value
            if not error_message:
                query1 = "select email,created from tokendata where token='{}'".format(token)
                cursor.execute(query1)
                str = cursor.fetchone()
                if not str:
                    error_message="Token not present in table"
                    return render(request, 'forgotpassword_page.html', {'error' : error_message})
                else: 
                    date = str[1]
                    formattedTime = date.strftime("%H:%M:%S")
                    now = datetime.now()
                    beforeTime = datetime.now()-timedelta(seconds=900)
                    beforeFormattedTime = beforeTime.strftime("%H:%M:%S")
                    if now.strftime("%m/%d/%Y") > date.strftime("%m/%d/%Y"):
                        if beforeFormattedTime > formattedTime:
                            error_message = "Token expired or used. Generate new token"
                            query2 = "delete from tokendata where token='{}'".format(token)
                            cursor.execute(query2)
                            m.commit()
                            return render(request, 'forgotpassword_page.html', {'error' : error_message})
                    else:
                        email = str[0]
                        query = "update users set password='{}' where email='{}'".format(password, email)
                        cursor.execute(query)
                        m.commit()
                        query2 = "delete from tokendata where token='{}'".format(token)
                        cursor.execute(query2)
                        m.commit()
                        return render(request, 'resetpassword_page.html')
            else:
                return render(request, 'resetpassword_page.html', {'error' : error_message})
        else:
            return render(request, 'resetpassword_page.html')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)