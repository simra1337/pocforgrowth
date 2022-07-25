from curses import keyname
from distutils.log import error
from django.shortcuts import render
from dotenv import load_dotenv
import mysql.connector as sql
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.
email=''
pwd=''
load_dotenv()

@csrf_exempt
def loginAction(request) :
    global email, pwd
    if request.method=='POST':
        m=sql.connect(host=os.getenv('HOST', default='localhost'), user=os.getenv('DBUSER'), passwd=os.getenv('PASSWORD'), database = os.getenv('DATABASE'))
        cursor = m.cursor()
        d=request.POST
        error_message=''
        for key,value in d.items():
            if key=="email":
                if not value:
                    error_message = "Email required"
                elif not value.__contains__('@'):
                    error_message = "Not valid email"
                else:
                    email = value
            if key=="password":
                if not value:
                    error_message = "Password required"
                elif len(value) < 6:
                    error_message = "Incorrect password. Password length should be more than 6"
                else:
                    pwd = value
        if not error_message:
            c="select * from users where email='{}' and password='{}'".format(email, pwd)
            cursor.execute(c)
            t = tuple(cursor.fetchall())
            if t==():
                return render(request, 'error_page.html')
            else:
                return render(request, 'welcome_page.html')
        else:
            return render(request, 'login_page.html', {'error': error_message})
    return render(request, 'login_page.html')