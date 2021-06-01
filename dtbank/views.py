from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import django.contrib.auth.hashers as hasher
from django.shortcuts import redirect
from django.db import connection
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

# Create your views here.

def home(request):
	return render(request, 'home.html', {'title': 'Home'})


def userloginpage(request):
	return render(request, 'login.html')

def managerloginpage(request):
	return render(request, 'managerlogin.html')

def login(request):
	username = request.POST.get('username')	#check if username exists in database
	institution = request.POST.get('institution')
	password = request.POST.get('password')

	cursor = connection.cursor()
	query = "select password from User_Work where username='"+username+"' and institution_name='"+institution+"'"
	cursor.execute(query)
	encodedtuple = cursor.fetchall()
	if len(encodedtuple)==0:
		return render(request, 'login.html', {'message': "Invalid username or password!"})

	encoded = encodedtuple[0][0]		#check if there is any value

	if hasher.check_password(password, encoded):	#check database user - password
		return render(request, 'userhome.html', {'username':username})
	else:
		return render(request, 'login.html', {'message': "Invalid username or password!"})

def managerlogin(request):
	username = request.POST.get('username')	#check if username exists in database
	password = request.POST.get('password')
	#if hasher.check_password(password, encoded): #check database manager - password
	cursor = connection.cursor()
	query = "select password from Database_Manager where username='"+username+"'"
	cursor.execute(query)
	encodedtuple = cursor.fetchall()
	if len(encodedtuple)==0:
		return render(request, 'managerlogin.html', {'message': "Invalid username or password!"})
		
	encoded = encodedtuple[0][0]		#check if there is any value

	if hasher.check_password(password, encoded):
		return render(request, 'managerhome.html', {'message':'Welcome '+username+"!"})
	else:
		return render(request, 'managerlogin.html', {'message': "Invalid username or password!"})

def userhome(request, username):
	return render(request, 'userhome.html', {'message':'Welcome '+username+"!"})

def managerhome(request, username):
	return render(request, 'managerhome.html', {'message':'Welcome '+username+"!"})

def createtables(request):
	with connection.cursor() as c:
    		c.execute("CREATE TABLE User ( password	CHAR(30), username	CHAR(20) NOT NULL, institution CHAR(100), PRIMARY KEY(username,institution))")

def saveuser(request):
	username = request.POST.get('username')
	name = request.POST.get('name')
	institution = request.POST.get('institution')
	password = request.POST.get('password')
	encoded = hasher.make_password(password, hasher='pbkdf2_sha256')		#save the username, institution name and the encrypted to database
	cursor = connection.cursor()
	insertion = "insert into User_Work values ('"+encoded+"','"+name+"','"+username+"','"+institution+"')"
	cursor.execute(insertion)
	return render(request,'managerhome.html', {'message':"User saved successfully!"})

def adduser(request):
	return render(request, 'adduser.html')

def encrypt_passwords(request):
	cursor = connection.cursor()			#encode database manager passwords
	cursor.execute("select username, password from Database_Manager")
	user_password = cursor.fetchall()

	for username, password in user_password:
		encoded = hasher.make_password(password)
		query = "update Database_Manager set password='"+encoded+"' where username='"+username+"'"
		cursor.execute(query)

	cursor.execute("select username, institution_name, password from User_Work")	#encode user passwords
	user_password = cursor.fetchall()

	for username, institution, password in user_password:
		encoded = hasher.make_password(password)
		query = "update User_Work set password='"+encoded+"' where username='"+username+"' and institution_name= '"+institution+"'"
		cursor.execute(query)

	return redirect('home')










