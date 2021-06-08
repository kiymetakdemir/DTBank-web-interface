from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import django.contrib.auth.hashers as hasher
from django.shortcuts import redirect
from django.db import connection
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view


cursor = connection.cursor()
#
#	*** User Operations
#
def viewDrugInfo(request):
	cursor.execute("select drugbank_id, drug_name, smiles, description from Drug")
	drugs = cursor.fetchall()

	cursor.execute("select D.drugbank_id, D.drug_name,D.smiles, D.description, U.target_name  from Drug D, Reaction_Related R, UniProt U where D.drugbank_id=R.drugbank_id and R.uniprot_id=U.uniprot_id")
	targets = cursor.fetchall()
	cursor.execute("select D.drugbank_id, D.drug_name,D.smiles, D.description, S.side_effect_name  from Drug D, Sider_Has S where D.drugbank_id=S.drugbank_id")
	sides = cursor.fetchall()
	
	columns = ["Drugbank ID", "Drug Name", "Smiles", "Description", "Target Name", "Side Effect Name"]

	dct = {drug:[[],[]] for drug in drugs}

	for tpl in targets:
		dct[(tpl[0],tpl[1], tpl[2], tpl[3])][0].append(tpl[4])

	for tpl in sides:
		dct[(tpl[0],tpl[1], tpl[2], tpl[3])][1].append(tpl[4])

	tuples = [(k[0],k[1], k[2], k[3], v[0], v[1]) for k,v in dct.items()]

	return render(request, "viewtable.html", {'tuples':tuples, 'columns':columns})


def viewdruginteractions(request):
	drugbank_id = request.POST.get('id')
	cursor.execute("select drugbank_id_2 from Interaction_with where drugbank_id_1 = '"+drugbank_id+"'")
	ts = cursor.fetchall()
	interactions = [t[0] for t in ts]
	names = []
	for drug in interactions:
		cursor.execute("select drug_name from Drug where drugbank_id='"+drug+"'")
		names.append(cursor.fetchall()[0])
	names = [name[0] for name in names]

	tuples = []
	for i in range(len(interactions)):
		tuples.append((interactions[i],names[i]))

	return render(request,"viewtable.html", {'tuples':tuples, 'columns':["Drug id", "Drug name"]})

def viewSideEffects(request):
	drugbank_id = request.POST.get('id')
	cursor.execute("select side_effect_name, umls_cui from Sider_Has where drugbank_id = '"+drugbank_id+"'")
	tuples = cursor.fetchall()
	
	return render(request,"viewtable.html", {'tuples':tuples, 'columns':["Side Effect Name", "UMLS CUI"]} )

def viewdruginteractingtargets(request):
	drugbank_id = request.POST.get('id')
	cursor.execute("select uniprot_id from Reaction_Related where drugbank_id = '"+drugbank_id+"' ")
	ts = cursor.fetchall()
	interacting=[t[0] for t in ts]
	names=[]
	for prot in interacting:
		cursor.execute("select target_name from Uniprot where uniprot_id='"+prot+"'")
		names.append(cursor.fetchall()[0])
	names = [name[0] for name in names]
	tuples = []
	for i in range(len(interacting)):
		tuples.append((interacting[i],names[i]))
	
	return render(request,"viewtable.html", {'tuples':tuples, 'columns':["Uniprot ID","Target Name"]} )

def viewproteininteractings(request):
	uniprot_id = request.POST.get('id')
	cursor.execute("select drugbank_id  from Reaction_Related where uniprot_id = '"+uniprot_id+"'")
	ts = cursor.fetchall()
	interacting=[t[0] for t in ts]
	names=[]
	for drug in interacting:
		cursor.execute("select drug_name from Drug where drugbank_id='"+drug+"'")
		names.append(cursor.fetchall()[0])
	names = [name[0] for name in names]

	tuples = []
	for i in range(len(interacting)):
		tuples.append((interacting[i],names[i]))
	
	return render(request,"viewtable.html", {'tuples':tuples, 'columns':["Interacting Drugs", "Drug Name"]} )

def sameproteindrugs(request):
	cursor.execute("select uniprot_id from Uniprot")
	prots= cursor.fetchall()
	keys = []
	for prot in prots:
		keys.append(prot[0])
	dct = {key:[] for key in keys}

	cursor.execute("select distinct(R1.drugbank_id), R1.uniprot_id from Reaction_Related R1, Reaction_Related R2  where R1.uniprot_id = R2.uniprot_id")
	tuples = cursor.fetchall()
	
	for tpl in tuples:
		
		dct[tpl[1]].append(tpl[0])

	tuples = [(k,v) for k,v in dct.items()]
	columns = ["Uniprot ID","Drugs That Affect"]
	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})
def samedrugproteins(request):
	cursor.execute("select drugbank_id from Drug")
	drugs= cursor.fetchall()
	keys = []
	for drug in drugs:
		keys.append(drug[0])
	dct = {key:[] for key in keys}

	cursor.execute("select distinct(R1.uniprot_id), R1.drugbank_id from Reaction_Related R1, Reaction_Related R2  where R1.drugbank_id = R2.drugbank_id")
	tuples = cursor.fetchall()
	
	for tpl in tuples:
		
		dct[tpl[1]].append(tpl[0])

	tuples = [(k,v) for k,v in dct.items()]
	columns = ["DrugBank ID","Proteins That Bind"]
	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})	

def viewdrugswithsider(request):
	umls_cui = request.POST.get('id')
	cursor.execute("select drugbank_id, side_effect_name from Sider_Has where umls_cui = '"+umls_cui+"'")
	tuples = cursor.fetchall()
	
	return render(request,"viewtable.html", {'tuples':tuples, 'columns':["DrugBank ID", "Side Effect Name"]} )

def searchandviewdrugs(request):
	keyword = request.POST.get('id')
	cursor.execute("select drugbank_id, drug_name, description from Drug where description like CONCAT('%', '"+keyword+"', '%');")
	tuples = cursor.fetchall()
	
	return render(request,"viewtable.html", {'tuples':tuples, 'columns':["DrugBank ID", "Drug Name", "Description"]} )	
def rankinstitutes(request):
	cursor.execute("select institution_name, score from Institution order by score desc")
	tuples= cursor.fetchall()
	
	columns = ["Institute","Score"]
	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})		

#
#   *** GENERAL
#

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

	query = "select password from User_Work where username='"+username+"' and institution_name='"+institution+"'"
	cursor.execute(query)
	encodedtuple = cursor.fetchall()
	if len(encodedtuple)==0:
		return render(request, 'login.html', {'message': "Invalid username or password0!"})

	encoded = encodedtuple[0][0]		#check if there is any value

	if hasher.check_password(password, encoded):	#check database user - password
		return render(request, 'userhome.html', {'username':username})
	else:
		return render(request, 'login.html', {'message': "Invalid username or password1!"})

def managerlogin(request):
	username = request.POST.get('username')	#check if username exists in database
	password = request.POST.get('password')
	#if hasher.check_password(password, encoded): #check database manager - password
	query = "select password from Database_Manager where username='"+username+"'"
	cursor.execute(query)
	encodedtuple = cursor.fetchall()
	if len(encodedtuple)==0:
		return render(request, 'managerlogin.html', {'message': "Invalid username or password0!"})
		
	encoded = encodedtuple[0][0]		#check if there is any value

	if hasher.check_password(password, encoded):
		return render(request, 'managerhome.html', {'message':'Welcome '+username+"!"})
	else:
		return render(request, 'managerlogin.html', {'message': "Invalid username or password1!"})

def userhome(request, username):
	return render(request, 'userhome.html')

def managerhome(request):
	return render(request, 'managerhome.html')

#
#	*** Database Manager operations
#
def saveuser(request):
	username = request.POST.get('username')
	name = request.POST.get('name')
	institution = request.POST.get('institution')
	password = request.POST.get('password')
	encoded = hasher.make_password(password, hasher='pbkdf2_sha256')		#save the username, institution name and the encrypted to database
	insertion = "insert into User_Work values ('"+encoded+"','"+name+"','"+username+"','"+institution+"')"
	cursor.execute(insertion)
	return render(request,'managerhome.html', {'message':"User saved successfully!"})

def update_affinity(request):
	reaction_id = request.POST.get('id')
	newvalue = request.POST.get('affinity')
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
	cursor.execute("select * from UniProt where uniprot_id= '"+uniprot_id+"'")
	temp = cursor.fetchall()
	if len(temp)==0:
		return render(request, 'managerhome.html', {'message':"There is no protein with the given id. Please try again."})
	else:
		deletion = "delete from UniProt where uniprot_id= '"+uniprot_id+"'"
		cursor.execute(deletion)
		return render(request,'managerhome.html', {'message':"Protein deleted successfully!"})

def viewtable(request, tablename):
	query = "select * from "+tablename
	cursor.execute(query)
	tuples = cursor.fetchall()
	cursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= N'"+tablename+"'")
	columns = cursor.fetchall()
	columns = [col for (col,) in columns]
	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})

def viewusers(request):		#wrote a new function to not to get passwords
	cursor.execute("select name, username, institution_name from User_Work")
	tuples = cursor.fetchall()
	columns = ["name", "username", "institution"]
	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})

def viewpapers(request):
	cursor.execute("select T1.doi, T1.institution_name, T3.name from Article_Institution T1, Article_Author T2, User_Work T3 where T1.doi = T2.doi and T2.username=T3.username and T1.institution_name=T3.institution_name")
	tuples = cursor.fetchall()
	columns = ["doi", "institution", "authors"]
	articles = []
	for tpl in tuples:
		if (tpl[0],tpl[1]) not in articles:
			articles.append((tpl[0],tpl[1]))

	dct = {article:[] for article in articles}

	for tpl in tuples:
		dct[(tpl[0],tpl[1])].append(tpl[2])

	tuples = [(k[0],k[1],v) for k,v in dct.items()]

	return render(request, 'viewtable.html', {'tuples':tuples, 'columns': columns})

def updateContributors(request):
	reaction_id = request.POST.get("reaction_id")
	cursor.execute("select doi from Reaction_Related where reaction_id= '"+reaction_id+"'")
	doi = cursor.fetchall()
	if len(doi)==0:
		return render(request, 'managerhome.html', {'message':"There is no reaction with the given id. Please try again."})
	else:
		doi=doi[0][0]
		cursor.execute("select username from Article_Author where doi='"+doi+"'")
		authors = cursor.fetchall()
		cursor.execute("select institution_name from Article_Institution where doi='"+doi+"'")
		institution = cursor.fetchall()[0][0]
		return render(request, 'updatecontributors.html', {'reaction_id':reaction_id, 'doi':doi, 'authors':authors, 'institution':institution})

def addauthors(request, doi, reaction_id):
	username = request.POST.get('username')
	name = request.POST.get('name')
	cursor.execute("select institution_name from Article_Institution where doi='"+doi+"'")
	institution = cursor.fetchall()[0][0]
	password = request.POST.get('password')
	encoded = hasher.make_password(password, hasher='pbkdf2_sha256')		#save the username, institution name and the encrypted to database 
	cursor.execute("insert into User_Work values ('"+encoded+"','"+name+"','"+username+"','"+institution+"')")
	cursor.execute("insert into Article_Author values ('"+doi+"','"+username+"')")
	cursor.execute("select username from Article_Author where doi='"+doi+"'")
	authors = cursor.fetchall()
	cursor.execute("select institution_name from Article_Institution where doi='"+doi+"'")
	institution = cursor.fetchall()[0][0]
	return render(request, 'updatecontributors.html', {'reaction_id':reaction_id, 'doi':doi, 'authors':authors, 'institution':institution, 'message':"Author added successfully!"})

def addUserAsAuthor(request, doi, reaction_id):
	username = request.POST.get('username')

	cursor.execute("select institution_name from Article_Institution where doi='"+doi+"'")
	institution = cursor.fetchall()[0][0]

	cursor.execute("select username from Article_Author where doi='"+doi+"'")
	authors = cursor.fetchall()

	cursor.execute("select * from User_Work where institution_name='"+institution+"' and username='"+username+"'")
	check = cursor.fetchall()

	if len(check)>0:
		insertion = "insert into Article_Author values ('"+doi+"','"+username+"')"
		cursor.execute(insertion)
		cursor.execute("select username from Article_Author where doi='"+doi+"'")
		authors = cursor.fetchall()
		return render(request, 'updatecontributors.html', {'reaction_id':reaction_id, 'doi':doi, 'authors':authors, 'institution':institution, 'message':"Author added successfully!"})
	else:
		return render(request, 'updatecontributors.html', {'reaction_id':reaction_id, 'doi':doi, 'authors':authors, 'institution':institution, 'message':"There is no such user. Please add as a new user."})

def removeauthor(request, doi, username, reaction_id):
	cursor.execute("select username from Article_Author where doi='"+doi+"'")
	authors = cursor.fetchall()
	cursor.execute("select institution_name from Article_Institution where doi='"+doi+"'")
	institution = cursor.fetchall()[0][0]

	if len(authors)<=1:
		return render(request, 'updatecontributors.html', {'reaction_id':reaction_id, 'doi':doi, 'authors':authors, 'institution':institution, 'message':"There should be at least 1 author!"})
	else:
		delete = "delete from Article_Author where username= '"+username+"' and doi='"+doi+"'"
		cursor.execute(delete)
		cursor.execute("select username from Article_Author where doi='"+doi+"'")
		authors = cursor.fetchall()
		return render(request, 'updatecontributors.html', {'reaction_id':reaction_id, 'doi':doi, 'authors':authors, 'institution':institution, 'message':"Author removed successfully!"})


def encrypt_passwords(request):
			#encode database manager passwords
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

#
#
#








