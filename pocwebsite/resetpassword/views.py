from distutils.log import error
from django.shortcuts import render
import mysql.connector as sql
import os
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

cpass = ''
password= ''

@csrf_exempt
def resetPasswordAction(request, token):
    global password, cpass
    if request.method == 'POST':
        m=sql.connect(host=os.getenv('HOST', default='localhost'), user=os.getenv('DBUSER'), passwd=os.getenv('PASSWORD'), database = os.getenv('DATABASE'))
        cursor = m.cursor()
        d = request.POST
        error_message=''
        #query1 = "select token from tokendata where email='{}'".format(email)
        #cursor.execute(query1)
        #str = cursor.fetchone()
        #token = ''.join(str)
        #error_message = ''
        #print("===============================+?")
        #if not token:
            #error_message = "Token expired or used"
            #print("===============================+2")
            #return render(request, 'forgotpassword_page.html')
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
            query1 = "select email from tokendata where token='{}'".format(token)
            cursor.execute(query1)
            str = cursor.fetchone()
            if not str:
                error_message = "Token expired or used."
                return render(request, 'forgotpassword_page.html', {'error' : error_message})
            else:
                email = ''.join(str)
                query = "update users set password='{}' where email='{}'".format(password, email)
                print(cursor.execute(query))
                m.commit()
                query2 = "delete from tokendata where token='{}'".format(token)
                cursor.execute(query2)
                m.commit()
                return render(request, 'resetpassword_page.html')
        else:
            return render(request, 'resetpassword_page.html', {'error': error_message})
    return render(request, 'resetpassword_page.html')
