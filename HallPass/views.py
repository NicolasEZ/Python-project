from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Celeb
from serpapi.google_search_results import GoogleSearchResults

def index(request):
    return render(request, "login.html")

def registerpage(request):
    return render(request, "registerpage.html")

def register(request):
	errors = User.objects.registration_validator(request.POST)
	if len(errors) > 0:
		for key, val in errors.items():
			messages.error(request, val)
		return redirect("/")

	pw = request.POST['password']
	pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
	new_user = User.objects.create(
		first_name = request.POST['fname'],
		last_name = request.POST['lname'],
		email = request.POST['email'],
		password = pw_hash
	)
	request.session['userid'] = new_user.id
	return redirect("/celebs/new")

def friends(request):
    if "userid" not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.filter(id=request.session['userid'])[0]
    }

    return render(request, "friends.html", context)

def myhallpass(request):
    if "userid" not in request.session:
        return redirect("/")

    # yourcelebs=User.objects.get(id=request.session['userid']).celebs.all()

    context = {
        "user": User.objects.filter(id=request.session['userid'])[0],
        "celebs": Celeb.objects.filter(users=request.session['userid']).order_by("ranking"),
        "allcelebs": Celeb.objects.all().order_by("ranking"),
    }
    return render(request, "myhallpass.html", context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")

    user = User.objects.filter(email=request.POST['email'])[0]
    request.session['userid'] = user.id
    return redirect("/myhallpass")

def logout(request):
    del request.session["userid"]
    return redirect("/")

def newceleb(request):
    if "userid" not in request.session:
        return redirect("/")

    context = {
        "user": User.objects.filter(id=request.session['userid'])[0]
    }
    return render(request, "newceleb.html", context)

def processnewceleb(request):
    errors = Celeb.objects.celebvalidator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/celebs/new")

    celeb = Celeb.objects.create(
        ranking=request.POST['ranking'],
        photo=request.POST['photo'],
        name=request.POST['name'],
        comments=request.POST['comments'],
    )
    currentuser=request.session['userid']
    celeb.users.add(currentuser)
    return redirect("/myhallpass")

def destroy(request, id):
    celeb = Celeb.objects.get(id=id)
    celeb.delete()
    return redirect("/myhallpass")

def edit(request, id):
    context = {
        "celeb": Celeb.objects.get(id=id),
        "user": User.objects.filter(id=request.session['userid'])[0]
    }
    return render(request, "edit.html", context)

def update(request, id):
    errors = Celeb.objects.celebvalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/celebs/edit/{id}')
    else:
        celeb = Celeb.objects.get(id=id)
        celeb.ranking = request.POST['ranking']
        celeb.photo = request.POST['photo']
        celeb.name = request.POST['name']
        celeb.comments = request.POST['comments']
        celeb.save()
        return redirect("/myhallpass")

def removefromlist(request, id):
    celebtoremove = Celeb.objects.get(id=id)
    currentuser=request.session['userid']
    celebtoremove.users.remove(currentuser)
    return redirect('/myhallpass')

def addtolist(request, id):
    celebtoadd = Celeb.objects.get(id=id)
    currentuser=request.session['userid']
    celebtoadd.users.add(currentuser)
    return redirect('/myhallpass')

def friends(reqeust):
    return redirect('/myhallpass')