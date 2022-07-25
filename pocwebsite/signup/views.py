from ast import IsNot
from curses import keyname
from distutils.log import error
from lib2to3.pgen2.token import NOTEQUAL
from django.shortcuts import render
import mysql.connector as sql
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

# Create your views here.
fn=''
ln=''
email=''
ph=''
pwd=''
load_dotenv()

@csrf_exempt
def signupAction(request) :
    global fn, ln, email, ph, pwd
    if request.method=='POST':
        #m=sql.connect(host="localhost", user="root", passwd="ttn", database = 'growthpoc')
        m=sql.connect(host=os.getenv('HOST', default='localhost'), user=os.getenv('DBUSER', default='root'), passwd =os.getenv('PASSWORD'), database=os.getenv('DATABASE'))
        cursor = m.cursor()
        d=request.POST
        error_message = ''
        for key,value in d.items():
            if key=="first_name":
                if not value:
                    error_message = "First name required"
                elif len(value) < 5:
                    error_message = "First name length should be more than 5"
                else:
                    fn = value
            if key=="last_name":
                if not value:
                    error_message = "Last name required"
                elif len(value) <5:
                    error_message = "Last name length should be more than 5"
                else:
                    ln = value
            if key=="email":
                if not value:
                    error_message = "Email required"
                elif not value.__contains__('@'):
                    error_message = "Not valid email"
                else:
                    email = value
            if key=="phone":
                if not value:
                    error_message = "Phone number required"
                elif len(value)<10 or len(value)>12:
                    error_message = "Phone number length should not be less than 10 and greator than 12"
                else:
                    ph = value
            if key=="password":
                if not value:
                    error_message = "Password required"
                elif len(value) <6:
                    error_message = "Password length should be more than 6"
                else:
                    pwd = value
            if key=="cpassword":
                if value!=pwd:
                    error_message = "Passwords do not match"
        if not error_message:
            c="insert into users Values('{}','{}','{}','{}','{}')".format(fn,ln,email,ph,pwd)
            cursor.execute(c)
            m.commit()
            return render(request, 'signup_page.html')
        else:
            return render(request, 'signup_page.html', {'error' : error_message})
    return render(request, 'signup_page.html')