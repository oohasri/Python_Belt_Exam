from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
	return render(request, "job/index.html")

def register(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors) > 0:
		for key,value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		user_check = User.objects.filter(email=request.POST["email"])
		if not user_check:
			password = request.POST["password"]
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # create the hash    
			print(pw_hash)      
			user = User.objects.create(first_name=request.POST["first_name"],
				last_name=request.POST["last_name"],
				email=request.POST["email"],
				password=pw_hash)
			request.session['userid'] = user.id
			request.session['first_name'] = user.first_name
			return redirect("/login_success")
		else:
			errors["user_exists"] = "User already exists"
			if len(errors) > 0:
				for key,value in errors.items():
					messages.error(request, value)
				return redirect("/")

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors) > 0:
		for key,value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		username = request.POST['email']
		password = request.POST['password']
		user = User.objects.filter(email=request.POST["email"])
		if user:
			logged_user = user[0]
			if bcrypt.checkpw(request.POST["password"].encode(), logged_user.password.encode()):
				request.session['userid'] = logged_user.id
				request.session['first_name'] = logged_user.first_name
				return redirect('/login_success')
		return redirect("/")

def user_wall(request):
	if 'userid' in request.session:
		dict= {
			'jobs' : Job.objects.all().order_by("-created_at"),
		}	
		return render(request, "job/wall.html", dict)
	else:
		return redirect("/")
def success(request):
	if 'userid' in request.session:
		return redirect("/dashboard")
	else:
		return redirect("/")

def add_job(request):
	if 'userid' in request.session:
		return render(request, "job/add_job.html")
	else:
		return redirect("/")

def job_post(request):
	if 'userid' in request.session:
		errors = User.objects.job_validator(request.POST)
		if len(errors) > 0:
			for key,value in errors.items():
				messages.error(request, value)
			return redirect("jobs/new")
		else:
			print(request.POST["description"])
			this_user = User.objects.filter(id=request.session["userid"])
			Job.objects.create(user=this_user[0], title=request.POST["title"], description=request.POST["description"], location=request.POST["location"])
			return redirect("/dashboard")
	else:
		return redirect("/")

def display_job(request, my_val):
	if 'userid' in request.session:		
		dict = {
		 	"jobs":Job.objects.filter(id=my_val),
		}
		return render(request, "job/display_job.html", dict)
	else:
		return redirect("/")

def edit_job(request, my_val):
	if 'userid' in request.session:	
		dict  = {
			"jobs" : Job.objects.filter(id=my_val),
		}	
		return render(request, "job/edit_job.html", dict)
	else:
		return redirect("/")

def post_editjob(request):
	if 'userid' in request.session:
		errors = User.objects.job_validator(request.POST)
		if len(errors) > 0:
			for key,value in errors.items():
				messages.error(request, value)
			return redirect("/jobs/edit/"+request.POST["job_id"])
		else:
			this_job = Job.objects.filter(id=request.POST["job_id"])
			if this_job:
				this_job[0].title = request.POST["title"]
				this_job[0].description = request.POST["description"]
				this_job[0].location = request.POST["location"]
				this_job[0].save()
				return redirect("/dashboard")
	else:
		return redirect("/")

def delete_job(request, my_val):
	if 'userid' in request.session:	
		this_job = Job.objects.filter(id=my_val)
		if this_job:
			this_job[0].delete()
			return redirect("/dashboard")
	else:
		return redirect("/")

def destroy(request):
	request.session.flush()
	return redirect("/")
# Create your views here.
