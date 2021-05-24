from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import django.contrib.auth.hashers as hasher
from django.shortcuts import redirect
from django.db import connection
# Create your views here.

def home(request):
	return render(request, 'dtbank/home.html', {'title': 'Home'})


def userloginpage(request):
	return render(request, 'dtbank/userlogin.html')

def managerloginpage(request):
	return render(request, 'dtbank/managerlogin.html')

def login(request):
	username = request.POST.get('username')	#check if username exists in database
	encoded = ""	#takes the value of password of username
	password = request.POST.get('password')
	#if hasher.check_password(password, encoded): #check database manager - password
	if hasher.check_password(password, encoded):
		return render(request, 'dtbank/userhome.html', {'username':username})
	else:
		return render(request, 'dtbank/login.html', {'message': "Invalid username or password!"})

def managerlogin(request):
	username = request.POST.get('username')	#check if username exists in database
	encoded = ""	#takes the value of password of username
	password = request.POST.get('password')
	#if hasher.check_password(password, encoded): #check database manager - password
	if hasher.check_password(password, encoded):
		return render(request, 'dtbank/managerhome.html', {'username':username})
	else:
		return render(request, 'dtbank/managerlogin.html', {'message': "Invalid username or password!"})

def userhome(request, username):
	return render(request, 'dtbank/userhome.html', {'username':username})

def managerhome(request, username):
	return render(request, 'dtbank/managerhome.html', {'username':username})


"""def adduser(request):
	form = UserCreationForm(request.POST)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		username = form.cleaned_data.get('password')
		messages.success(request, f'Account created for {username}!')
		return redirect('dtbank-adduser')
	else:
		form = UserCreationForm()
	return render(request, 'dtbank/adduser.html', {'form': form})"""

"""def my_custom_sql(request):
	cursor = connection.cursor()
	cursor.execute("select name from demo")
	names = cursor.fetchall()
	return render(request, 'dtbank/home.html', {'names':names})"""