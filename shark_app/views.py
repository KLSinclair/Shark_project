from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from django.contrib import messages 
from .models import *

def index(request): 
    return render(request, "index.html") # presents form to reg/login

def success(request): 
    if 'name' in request.session: # If someone is registered or logged in, let them go to success, if not, back to home you go!
        return render(request, "success.html")
    return redirect("/") # if they do /success in browser (GET request) no going to Success, shame on them! LOL

def register(request): # This is the "root route" just presents the form to reg or log in
    # Creating a New User on this form
    print(request.POST) # In (terminal) prints the new User's info 
    # validate the data the User typed in on the form they submitted a POST request
    errors = User.objects.validator(request.POST)
    print(errors) # my errors printed in terminal 
    if len(errors) > 0: # No errors allowed, Dude! Fix your stuff! 
        for key, value in errors.items(): # error messages I pass to the User
            messages.error(request, value)
        return redirect("/") # redirect user back to form to fix errors
# 📌 if the errors object is empty, that means there were no errors!

    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() # replace 'test' with request.POST['password]
    new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_password)
    # create a new User
    print(new_user, "This is my shiny new user!")
    request.session['name'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect("/success")

def login(request):
    # see if POST data from form matches a User from db if so log them in.
    logged_user = User.objects.filter(email = request.POST['email']) # .get() will get an error if it fails, .filter() won't 
    if len(logged_user) > 0: # That meas this person exists at the very least
        logged_user = logged_user[0] # Remember, this is a list we're getting
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()): # be sure to check for variable tweeks when I paste this line of code I copied
            print(logged_user, "logged user was signed in!")
            request.session['name'] = logged_user.first_name
            request.session['id'] = logged_user.id
            return redirect('/success') # This is the "home page"
    return redirect("/") # back to form if email/pw conflict

def logout(request):
    request.session.clear()
    return redirect("/")
