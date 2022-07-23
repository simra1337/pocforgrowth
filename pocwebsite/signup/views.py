from curses import keyname
from distutils.log import error
import re
from django.shortcuts import render
import mysql.connector as sql
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
fn=''
ln=''
email=''
ph=''
pwd=''

@csrf_exempt
def signupAction(request) :
    global fn, ln, email, ph, pwd
    if request.method=='POST':
        m=sql.connect(host="localhost", user="root", passwd="tata123", database = 'growthpoc')
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
                elif len(value) < 10:
                    error_message = "Phone number length should not be less than 10"
                else:
                    ph = value
            if key=="password":
                if not value:
                    error_message = "Password required"
                elif len(value) <6:
                    error_message = "Password length should be more than 6"
                else:
                    pwd = value
        if not error_message:
            c="insert into users Values('{}','{}','{}','{}','{}')".format(fn,ln,email,ph,pwd)
            cursor.execute(c)
            m.commit()
            return render(request, 'signup_page.html')
        else:
            return render(request, 'signup_page.html', {'error' : error_message})
    return render(request, 'signup_page.html')