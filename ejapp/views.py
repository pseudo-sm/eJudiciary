# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pyrebase
from django.shortcuts import render,HttpResponse, HttpResponseRedirect

config = {
    'apiKey': "AIzaSyBQtKDMBy_zKICw9pSHcc4ypSn9w4kc_JA",
    'authDomain': "ejudiciary-66067.firebaseapp.com",
    'databaseURL': "https://ejudiciary-66067.firebaseio.com",
    'projectId': "ejudiciary-66067",
    'storageBucket': "",
    'messagingSenderId': "783290318894"
  };
firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

# Create your views here.

def index(request):

    return render(request,"index.html")

def profile(request):

    return render(request,"profile.html")

def home(request):

    return render(request,"home.html")

def signup(request):

    fullname = request.POST.get("fullname")
    email = request.POST.get("email")
    password = request.POST.get("password")
    aadhar = request.POST.get("aadhar")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    auth.create_user_with_email_and_password(email,password)
    auth.sign_in_with_email_and_password(email,password)
    uid = auth.current_user["localId"]
    db.child("users").child("users").child(uid).update({"name":fullname, "email":email, "password":password, "aadhar":aadhar, "phone":phone, "address":address})
    return HttpResponseRedirect("/home/")
