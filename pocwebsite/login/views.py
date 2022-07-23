from curses import keyname
from django.shortcuts import render
import mysql.connector as sql
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
email=''
pwd=''

@csrf_exempt
def loginAction(request) :
    global email, pwd
    if request.method=='POST':
        m=sql.connect(host="localhost", user="root", passwd="tata123", database = 'growthpoc')
        cursor = m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="email":
                email = value
            if key=="password":
                pwd = value

        c="select * from users where email='{}' and password='{}'".format(email, pwd)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        if t==():
            return render(request, 'error_page.html')
        else:
            return render(request, 'welcome_page.html')
    return render(request, 'login_page.html')