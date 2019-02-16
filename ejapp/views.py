# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pyrebase
from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.contrib import auth as authe
from functools import wraps
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

def user_login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kw):
        if auth.current_user is None:
            return HttpResponseRedirect('')
        else:
            id = auth.current_user["localId"]
            type = db.child("users").child("users").child(id).get().val()
            if type is None:

                return HttpResponseRedirect('')
            else:
                return function(request, *args, **kw)
    return wrapper

def index(request):

    return render(request,"index.html")

def profile(request):

    return render(request,"profile.html")

@user_login_required
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
    db.child("users").child("users").child(uid).update({"name":fullname, "email":email, "aadhar":aadhar, "phone":phone, "address":address})
    return HttpResponseRedirect("/home/")

def login(request):

    users = list(dict(db.child("users").child("users").get().val()).keys())
    email = request.POST.get("email")
    password = request.POST.get("password")
    auth.sign_in_with_email_and_password(email,password)
    uid = auth.current_user["localId"]
    if uid in users:
        
        return HttpResponseRedirect('/home/')

def logout(request):
    auth.current_user = None
    authe.logout(request)
    return index(request)


def police_home(request):

    all_users=dict(db.child("users").child("users").get().val())
    names = []
    phones = []
    users = []
    case_nos = []
    firnos = []
    firsubjects = []
    firdescriptions = []
    firtimestamps = []
    policestations = []
    epochs = []
    pid = "patia police station"
    all_cases = dict(db.child("cases").get().val())
    for case in all_cases:
        if all_cases[case]["pid"] == pid:
            uid = all_cases[case]["uid"]
            users.append(uid)
            names.append(all_users[uid]["name"])
            phones.append(all_users[uid]["phone"])
            case_nos.append(case)
            firnos.append(all_users[uid]["cases"][case]["firno"])
            firsubjects.append(all_users[uid]["cases"][case]["firsubject"])
            firtimestamps.append(all_users[uid]["cases"][case]["firtimestamp"])
            policestations.append(all_users[uid]["cases"][case]["policestation"])
            firdescriptions.append(all_users[uid]["cases"][case]["firdescription"])
            epochs.append(all_users[uid]["cases"][case]["epoch"])

    context = zip(users,names,phones,case_nos,firnos,firsubjects,firtimestamps,policestations,firdescriptions,epochs)

    return render(request,"temp.html",{"context":context})
