from django.shortcuts import render, redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            hash_key = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'],email=request.POST['email'],password=hash_key)
            user = User.objects.filter(email=request.POST['email'])
            logged_user = user[0]
            request.session['user'] = logged_user.id 
            return redirect ('/quotes')
    else:
        return redirect ('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'])
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
                    request.session['user'] = logged_user.id 
                    return redirect('/quotes')
            else:
                return redirect('/')
    else:
        return redirect('/')

def qoutes(request):
    user_id = request.session['user']
    context ={
        "all_quotes" : Qoute.objects.all(),
        "user_info" : User.objects.get(id=user_id),
        "favorites" : User.objects.get(id=user_id).users.all()
    }
    return render (request,'dashboard.html',context)

def add_quote(request):
    errors = Qoute.objects.basic_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')
        else:
            user_id = request.session['user']
            Qoute.objects.create(author=request.POST['author'],description=request.POST['description'],posted_by=User.objects.get(id=user_id))
            added_quote = Qoute.objects.last()
            upload_user_id = User.objects.get(id=user_id)
            upload_user_id.users.add(added_quote)
            return redirect('/quotes')
    else:
        return redirect ('/quotes')

def user_quotes(request,user_id):
    user_info = User.objects.get(id=user_id)
    context = {
        'user_info' : user_info}
    return render(request,'user_quotes.html',context)

def edit_account(request,user_id):
    user_id = request.session['user']
    user_info = User.objects.get(id=user_id)
    context = {
        'user_info' : user_info}
    return render(request,'account.html',context)

def add_to_liked(request,quote_id):
    user_adding = User.objects.get(id=request.session['user'])
    quote_to_favorites = Qoute.objects.get(id=quote_id)
    quote_to_favorites.users_who_like.add(user_adding)
    return redirect('/quotes')

def delete_quote(request,quote_id):
    quote_to_delete = Qoute.objects.get(id=quote_id)
    quote_to_delete.delete()
    return redirect('/quotes')

def change_account(request):
    errors = User.objects.update_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/myaccount/'+str(request.session['user']))
        else:
            user_id = request.session['user']
            user_to_update = User.objects.get(id=user_id)
            user_to_update.first_name = request.POST['first_name']
            user_to_update.last_name = request.POST['last_name']
            user_to_update.email = request.POST['email']
            user_to_update.save()
            return redirect ('/myaccount/'+str(request.session['user']))

    else:
        return redirect ('/myaccount/'+str(request.session['user']))

def log_off(request):
    del request.session['user']
    return redirect ('/')