from django.shortcuts import render
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
import mysql.connector as sql
import os
from django.core.mail import send_mail
from django.dispatch import receiver
import uuid

# Create your views here.
email = ''
load_dotenv()
subject = os.getenv('SUBJECT')
sender = os.getenv('EMAIL_HOST_USER')
message = os.getenv('MESSAGE')

@csrf_exempt
def forgotpasswordAction(request) :
    global email
    if request.method == 'POST':
        m=sql.connect(host=os.getenv('HOST', default='localhost'), user=os.getenv('DBUSER'), passwd=os.getenv('PASSWORD'), database = os.getenv('DATABASE'))
        cursor = m.cursor()
        d = request.POST
        error_message = ''
        for key,value in d.items():
            if key=="email":
                if not value:
                    error_message = "Email required"
                elif not value.__contains__('@'):
                    error_message = "Invalid email"
                else:
                    email = value
        if not error_message:
            c="select * from users where email='{}'".format(email)
            cursor.execute(c)
            t = tuple(cursor.fetchall())
            if t==():
                return render(request, 'error_page.html')
            else:
                token = str(uuid.uuid4())
                c="insert into tokendata values('{}','{}')".format(token, email)
                print("sssssssssssssssssssssssssssssssssssssssss")
                print(c)
                cursor.execute(c)
                m.commit()
                emailSenderHelper(email,token)
        else:
            return render(request, 'forgotpassword_page.html', {'error': error_message})
    return render(request, 'forgotpassword_page.html')


def emailSenderHelper(email, token):
    send_mail(
	    subject,
		message + token,
		sender,
		['hashitest3@gmail.com'],
        fail_silently=False,
	)
