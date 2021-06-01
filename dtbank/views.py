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
	return redirect('login')

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

def update_affinity(request):
	reaction_id = request.POST.get('id')
	newvalue = request.POST.get('affinity')
	cursor = connection.cursor()
	cursor.execute("select * from Reaction_Related where reaction_id='"+reaction_id+"'")
	temp = cursor.fetchall()
	if len(temp)==0:
		return render(request, 'managerhome.html',{'message':"There is no reaction with the given reaction id. Please try again."})
	else:
		update = "update Reaction_Related set affinity_NM= '"+newvalue+"' where reaction_id= '"+reaction_id+"'"
		cursor.execute(update)
		return render(request,'managerhome.html', {'message':"Affinity value updated successfully!"})

def delete_drug(request):
	drugbank_id = request.POST.get('id')
	cursor = connection.cursor()
	cursor.execute("select * from Drug where drugbank_id= '"+drugbank_id+"'")
	temp = cursor.fetchall()
	if len(temp)==0:
		return render(request, 'managerhome.html', {'message':"There is no drug with the given id. Please try again."})
	else:
		deletion = "delete from Drug where drugbank_id= '"+drugbank_id+"'"
		cursor.execute(deletion)
		return render(request,'managerhome.html', {'message':"Drug deleted successfully!"})


def delete_protein(request):
	uniprot_id = request.POST.get('id')
	cursor = connection.cursor()
	cursor.execute("select * from UniProt where uniprot_id= '"+uniprot_id+"'")
	temp = cursor.fetchall()
	if len(temp)==0:
		return render(request, 'managerhome.html', {'message':"There is no protein with the given id. Please try again."})
	else:
		deletion = "delete from UniProt where uniprot_id= '"+uniprot_id+"'"
		cursor.execute(deletion)
		return render(request,'managerhome.html', {'message':"Protein deleted successfully!"})

def updateContributors(request):
	reaction_id = request.POST.get("reaction_id")
	cursor = connection.cursor()
	cursor.execute("select * from Reaction_Related where reaction_id= '"+reaction_id+"'")
	temp = cursor.fetchall()
	if len(temp)==0:
		return render(request, 'managerhome.html', {'message':"There is no reaction with the given id. Please try again."})
	else:
		return render(request, 'managerhome.html', {'message':"I will implement this part later."})

def viewtable(request, tablename):
	cursor = connection.cursor()
	query = "select * from "+tablename
	cursor.execute(query)
	tuples = cursor.fetchall()
	cursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= N'"+tablename+"'")
	columns = cursor.fetchall()
	columns = list(columns)
	if tablename=="Article_Author_of":		#changed username column name as first author
		columns[2]=('first author',)
	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})

def viewusers(request):		#wrote a new function to not to get passwords
	cursor = connection.cursor()
	cursor.execute("select name, username, institution_name from User_Work")
	tuples = cursor.fetchall()
	columns = [("name",), ("username",), ("institution",)]
	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})

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

	return redirect('managerhome')











