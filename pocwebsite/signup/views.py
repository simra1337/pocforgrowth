from curses import keyname
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
        for key,value in d.items():
            if key=="first_name":
                fn = value
            if key=="last_name":
                ln = value
            if key=="email":
                email = value
            if key=="phone":
                ph = value
            if key=="password":
                pwd = value

        c="insert into users Values('{}','{}','{}','{}','{}')".format(fn,ln,email,ph,pwd)
        cursor.execute(c)
        m.commit()
    return render(request, 'signup_page.html')