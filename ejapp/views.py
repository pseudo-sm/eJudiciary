# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pyrebase
from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.contrib import auth as authe
from functools import wraps
from random import randint
from datetime import datetime
import random
import json
from ejapp.triathon_text_similarity.prediction import *
from ejapp.triathon_text_similarity.similar_text import *
from similarity.cosine import Cosine
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import matplotlib.pyplot as plt



def find_accuracy(dataset_name = 'lawers200.csv', model_name = 'model200.pickle'):
    y_true = []
    y_pred = []
    ss_res = 0
    ss_total = 0
    sum_y_true = 0
    counter = 0
    dataset = pd.read_csv(dataset_name)
    #print(len(dataset))
    #print(type(dataset['Ratings']))
    for i in dataset['Score']:
        y_true.append(i)
    # loading the saved model
    pickle_in = open(model_name, 'rb')
    regressor = pickle.load(pickle_in)
    for i in range(0,200):
        each_row = dataset.iloc[i,:].values
        pred = regressor.predict([[each_row[0],each_row[1],each_row[2]]])
        #print(pred)
        y_pred.append(pred[0])
    #for i in dataset:
        #print(i)
    #print(y_pred)
    for i in range(0, 200):
        single_mse = (y_true[i] - y_pred[i])**2
        ss_res += single_mse
    print('residual sum of squares:',ss_res)


    for i in range(0, 200):
        sum_y_true += y_true[i]

    avg_y_true = sum_y_true/len(dataset)
    #print(avg_y_true) #3.03759044807835

    for i in range(0, 200):
        tot_sum = (y_true[i] - avg_y_true)**2
        #print(tot_sum)
        ss_total += tot_sum

    #print(ss_total)

    #R2 error
    r2 = 1 - (ss_res/ss_total)
    print('accuracy', r2*100)
    #print('true val', y_true)
    #print('pred', y_pred)

    #return r2

    #return mean_squared_error(y_true, y_pred,multioutput='uniform_average')
    '''y_pred = regressor.predict([[rating,wins,time_diff]])'''
    #print(y_true)
    #print(y_pred)


config = {
    'apiKey': firebase-api-key,
    'authDomain': "your-app.firebaseapp.com",
    'databaseURL': "https://your-app.firebaseio.com",
    'projectId': "your-app-id",
    'storageBucket': "",
    'messagingSenderId': "sender-id"
  };
firebase = pyrebase.initialize_app(config)
1
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
    csi = list(dict(db.child("users").child("csi").get().val()).keys())
    judge = list(dict(db.child("users").child("judge").get().val()).keys())
    email = request.POST.get("email")
    password = request.POST.get("password")
    type = request.POST.get("type")
    auth.sign_in_with_email_and_password(email,password)
    uid = auth.current_user["localId"]
    if uid in users:
        
        return HttpResponseRedirect('/home/')
    if uid in csi:

        return HttpResponseRedirect('/csi/')
    if uid in judge:

        return HttpResponseRedirect('/judge-dashboard/')

def judge_dashboard(request):

    cases = []
    users = dict(db.child("users").child("users").get().val())
    all_cases = dict(db.child("cases").get().val())
    firno = []
    firdesc = []
    charge = []
    seizure = []
    petition = []
    defend = []
    jcases = dict(db.child("users").child("judge").child('ALKP9FtuMSTDwFE07dRdIZxCCSc2').child("cases").get().val())
    cosine = Cosine(2)
    similar = {}
    for case in jcases:
        cases.append(case)
        uid = all_cases[case]["uid"]
        if users[uid]["cases"][case].get("firno") is not None:
            firno.append(users[uid]["cases"][case]["firno"])
            firdesc.append(users[uid]["cases"][case]["firdescription"])
            for cid in all_cases:
                m_uid = all_cases[cid]["uid"]
                similarity = cosine.similarity_profiles(cosine.get_profile(users[uid]["cases"][case]["firdescription"]), cosine.get_profile(users[m_uid]["cases"][cid]["firdescription"]))
                similar.update({cid:similarity})
            charge.append(','.join(list(users[uid]["cases"][case]["chargesheet"].keys())))
            seizure.append(users[uid]["cases"][case]["seizure list"])
        defend.append(users[uid]["advocate"])
        petition.append(users[uid]["name"])
    sorted_similar = sorted(similar,key=similar.get,reverse=True)
    lent = len(cases)
    context = zip(range(1,lent+1),cases,firno,firdesc,charge,seizure,defend,petition)
    print(cases,firno,firdesc,charge,seizure,defend,petition)
    add = zip(cases,firdesc)
    return render(request,"judge_dashboard.html",{"context":context,'add':add,'sorted_similar':sorted_similar})

def judge_update(request):

    date  = request.GET.get("date")
    desc = request.GET.get("desc")
    cid = request.GET.get('cid')
    cases = dict(db.child("cases").get().val())
    uid = cases[cid]["uid"]
    timestamp = int(datetime.timestamp(datetime.now()))
    db.child("users").child("users").child(uid).child("cases").child(cid).update({"next date":date,"date description":desc})
    db.child("users").child("users").child(uid).child("cases").child(cid).child("events").update({timestamp:"Dates Extended"})
    db.child("users").child("users").child(uid).child("cases").child(cid).update({"epoch":timestamp})
    db.child("cases").child(cid).update({"status":"hearing Date published"})
    all =True
    return HttpResponse(json.dumps(all),content_type="json/application")

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

    return render(request,"police_dashboard.html",{"context":context})


# def admin2(request):
#
#     all_cases = dict(db.child("cases").get().val())
#     csi = dict(db.child("users").child("csi").get().val())
#     all_users = dict(db.child("users").child("users").get().val())
#     uid = []
#     cid = []
#     pid = []
#     cname = []
#     cphone =[]
#     cemail=[]
#     caadhar=[]
#     caddress=[]
#     cases = {}
#     events = []
#     for key in all_cases:
#         cid.append(key)
#         cname.append(all_users[all_cases[key]["uid"]]["name"])
#         cphone.append(all_users[all_cases[key]["uid"]]["phone"])
#         cemail.append(all_users[all_cases[key]["uid"]]["email"])
#         caddress.append(all_users[all_cases[key]["uid"]]["address"])
#         caadhar.append(all_users[all_cases[key]["uid"]]["aadhar"])
#         uid=all_cases[key]["uid"]
#         cases.update(all_users[uid]["cases"])
#         events.append(all_users[uid]["cases"][key]["events"])
#     timelist = []
#     for event in events:
#         list1 = list(event.keys())
#         for case in list1:
#             print(case)
#
#     print(timelist)
#     data = zip(cid,cname,cphone,cemail,caadhar,caddress,events)
#     return render(request,"admin_temp.html",{"data":data})


def filefir(request):

    uid = auth.current_user["localId"]
    print(request.POST)
    subject = request.POST.get("firsubject")
    station = request.POST.get("station")
    description = request.POST.get("description")
    cid = randint(100000,999999)
    db.child("firs").child(cid).update({"uid":uid,"pid":station})
    db.child("cases").child(cid).update({"uid":uid,"pid":station})
    firno = randint(100000,999999)
    epoch = int(datetime.timestamp(datetime.now()))
    firtimestamp = int(datetime.timestamp(datetime.now()))
    db.child("users").child("users").child(uid).child('cases').child(cid).child("events").update({firtimestamp:"police"})
    db.child("users").child("users").child(uid).child("cases").child(cid).update({"epoch":epoch,"firdescription":description,"firno":firno,"firsubject":subject,"policestation":station,"firtimestamp":firtimestamp})
    return HttpResponseRedirect('/home/')


def auth_signup(request):

    return render(request,"higher_auth.html")

def advocate(request):
    name = request.POST.get("fullname")
    email = request.POST.get("email")
    password = request.POST.get("password")
    license = request.POST.get("license")
    aadhar = request.POST.get("aadhar")
    phone = request.POST.get("phone")
    category = request.POST.get("category")
    region = request.POST.get("region")
    auth.create_user_with_email_and_password(email, password)
    auth.sign_in_with_email_and_password(email, password)
    uid = auth.current_user["localId"]

    db.child("users").child("advocate").child(uid).update({"referral":'xyz123',"name":name,"email":email,"license":license,"aadhar":aadhar,"phone":phone,"category":category,"region":region})
    return render(request,"advocate_dashboard.html")

def judge(request):
    name = request.POST.get("fullname")
    email = request.POST.get("email")
    password = request.POST.get("password")
    aadhar = request.POST.get("aadhar")
    phone = request.POST.get("phone")
    district = request.POST.get("district")
    court = request.POST.get("court")
    auth.create_user_with_email_and_password(email, password)
    auth.sign_in_with_email_and_password(email, password)
    uid = auth.current_user["localId"]
    db.child("users").child("judge").child(uid).update({"name": name, "email": email,"aadhar": aadhar, "phone": phone, "district": district,"court": court})
    return HttpResponse("Welcome to judge's home.")

#
# def police_home(request):
#
#     auth.sign_in_with_email_and_password("police@gmail.com","password")
#     pid = auth.current_user["localId"]
#     all_firs = []
#     uids = []
#     firs = dict(db.child("firs").get().val())
#     for fir in firs:
#         all_firs.append(fir)
#         uids.append(firs[fir]["uid"])
#     context = zip(all_firs,uids)
#     return render(request,"tempPolice.html",{"context":context})

def police_manage(request):

    all_firs = dict(db.child("firs").get().val())
    users = dict(db.child("users").child("users").get().val())
    context_firs = []
    print(all_firs)
    for fir in all_firs:
        uid = all_firs[fir]["uid"]
        epoch = str(users[uid]["cases"][fir]["epoch"])
        status = users[uid]["cases"][fir]["events"][str(epoch)]
        if status == "police accepted":
            context_firs.append(fir)
    return render(request,"police_manage.html",{"context":context_firs})


def forward_csi(request):

    cases = dict(db.child("cases").get().val())
    seizure_list = request.POST.get("seizure")
    medical = request.POST.get("medical")
    fir = request.POST.get("fir")
    uid = cases[fir]["uid"]
    timestamp = int(datetime.timestamp(datetime.now()))
    db.child("users").child("users").child(uid).child("cases").child(fir).update({"seizure list":seizure_list,"medical report":medical})
    db.child("users").child("users").child(uid).child("cases").child(fir).child("events").update({timestamp:"csi"})
    db.child("users").child("users").child(uid).child("cases").child(fir).update({"epoch":timestamp})
    db.child("users").child("csi").child("rmPWzbkBDFNgKSBOBBXgblvCHYu2").child("cases").child(fir).update({uid:0})
    return HttpResponseRedirect('/police-manage/')

def submit_action(request):

    fir = request.GET.get("fir")
    print(fir)
    uid = db.child("firs").child(fir).child("uid").get().val()
    action = request.GET.get("action")
    reason = request.GET.get("reason")
    timestamp = int(datetime.timestamp(datetime.now()))
    if action == "accept":
        db.child("users").child("users").child(uid).child("cases").child(int(fir)).update({"epoch":timestamp})
        db.child("users").child("users").child(uid).child("cases").child(int(fir)).child("events").update({timestamp:"police accpeted"})
    else:
        db.child("users").child("users").child(uid).child("cases").child(int(fir)).update({"epoch":timestamp})
        db.child("users").child("users").child(uid).child("cases").child(fir).update({"reject":reason})
        db.child("users").child("users").child("cases").child(fir).child("events").update({timestamp:"police rejected"})
    all = True
    return HttpResponse(json.dumps(all),content_type="json/application")


def csi(request):

    csid = auth.current_user["localId"]
    case_nos = []
    case_subjects = []
    case_descriptions = []
    all_users = dict(db.child("users").child("users").get().val())
    all_cases = dict(db.child("users").child("csi").child(csid).child("cases").get().val())
    really_all_cases = dict(db.child("cases").get().val())
    case_list = list(all_cases.keys())
    all_firs = db.child("firs").get().val()
    for case in case_list:
        uid = really_all_cases[case]["uid"]
        case_nos.append(case)
        case_subjects.append(all_users[uid]["cases"][case]["firsubject"])
        case_descriptions.append(all_users[uid]["cases"][case]["firdescription"])
    context = zip(case_nos,case_subjects,case_descriptions)
    return render(request,"csi_dashboard.html",{"context":context})

def chargesheet(request):

    penal = request.GET.getlist('penal[]')
    cid = request.GET.get('cid')
    court = request.GET.get('court')
    all_cases = dict(db.child("cases").child(cid).get().val())
    uid = all_cases["uid"]
    timestamp = int(datetime.timestamp(datetime.now()))
    print(cid,uid)
    for p in penal:
        print(p)
        if p is not '':
            db.child('users').child("users").child(uid).child("cases").child(cid).child("chargesheet").update({p:0})
    db.child('users').child("users").child(uid).child("cases").child(cid).update({"court":court})
    db.child('users').child("users").child(uid).child("cases").child(cid).update({"epoch":timestamp})
    db.child('users').child("judge").child('ALKP9FtuMSTDwFE07dRdIZxCCSc2').child("cases").update({cid:0})
    db.child('users').child("users").child(uid).child("cases").child(cid).child("events").update({timestamp:"chargesheet filed"})
    db.child('cases').child(cid).update({"status":"chargesheet filed"})

    all = True
    return HttpResponse(json.dumps(all),content_type="json/application")

def auth_police(request):

    return render(request,"police_auth.html")

def statsupdate(request):

    case = request.POST.get("case").split(' ')
    case = case[0]
    status = request.POST.get("status")
    cases = db.child('cases').get().val()
    uid = cases[case]["uid"]
    timestamp = int(datetime.timestamp(datetime.now()))
    db.child('users').child('users').child(uid).child("cases").child(case).update({"current status":status})
    db.child('cases').child(case).update({"status":"next hearing Update"})
    db.child('users').child("users").child(uid).child("cases").child(case).child("events").update({timestamp:"Hearing Updates"})

    return HttpResponseRedirect('/judge-dashboard/')

def admin(request):

    users = dict(db.child("users").child("users").get().val())
    cases = dict(db.child("cases").get().val())
    casenos = []
    status = []
    epochs = []
    duration = []
    for case in cases:
        uid = cases[case]["uid"]
        casenos.append(case)
        latest_epoch = users[uid]["cases"][case]["epoch"]
        epochs.append(latest_epoch)
        print(latest_epoch)
        status.append(users[uid]["cases"][case]["events"][str(latest_epoch)])

    context = zip(casenos,status,epochs)
    return render(request,"admin2/index.html",{"context":context,"duration":duration})

def case_admin(request,case_no):

    case = dict(db.child("cases").child(case_no).get().val())
    uid = case["uid"]
    user = dict(db.child("users").child("users").child(uid).child("cases").child(case_no).get().val())
    court = user["court"]
    penal_codes = ','.join(list(user["chargesheet"].keys()))
    advocate = db.child("users").child("users").child(uid).child("advocate").get().val()
    current_status = user["current status"]
    firtimestamp = user["firtimestamp"]
    hearing_date = user["next date"]
    police_station = case["pid"]
    return render(request,"admin2/edit.html",{"case":case_no,"pid":police_station,"uid":uid,"court":court,"penal_codes":penal_codes,"advocate":advocate,"current_status":current_status,"firtimestamp":firtimestamp,"hearing_date":hearing_date})

def flagged_cases(request):

    users = dict(db.child("users").child("users").get().val())
    cases = dict(db.child("cases").get().val())
    flags = []
    pending = []
    init_date = []
    flagged_case = []
    for case in cases:
        uid = cases[case]["uid"]
        time_list = list(users[uid]["cases"][case]["events"].keys())
    diff = []

    try:
        for i in range(len(time_list)):
            diff.append(int(time_list[i+1])-int(time_list[i]))
    except IndexError:
        diff.append('-')
    for i in range(len(cases)):
        if diff[i]>45:
            flags.append({"caseno":case})
    for i in flags:
        case  =i["caseno"]
        uid = cases[case]["uid"]
        flagged_case.append(case)
        epoch = users[uid]["cases"][case]["epoch"]
        print(users[uid]["cases"][case]["events"])
        pending.append(users[uid]["cases"][case]["events"][str(epoch)])
        init_date.append(users[uid]["cases"][case]["firtimestamp"])
    context = zip(flagged_case,pending,init_date)
    return render(request,"admin2/flag.html",{"context":context})

def stats(request):

    advocates = dict(db.child("users").child("advocate").get().val())
    for adv in advocates:
        dataset_text = pd.read_csv('advocates.tsv', delimiter = '\t', quoting = 3)

        counter = 0
        input_list = []
        compare_list = []
        for i in range(0,1000):
            if dataset_text['Liked'][i] == 1:
                counter += 1
                if counter < 41:
                    input_list.append(dataset_text['Review'][i])
                    #print(input_text)

        final_text_str = ''.join(input_list)
        for i in range(1000):
            if dataset_text['Liked'][i] == 1:
                counter += 1
                if counter > 41:
                    compare_list.append(dataset_text['Review'][i])
                    #print(input_text)

        final_compare_text_str = ''.join(compare_list)

        pred = prediction()
        # pred.generate_a_dataset(qnt_of_rand_num = 200, dataset_name = 'lawers200.csv')
        # pred.train_model(csv_file = 'lawers200.csv', save_model_name = 'model200.pickle')
        diff = random.randint(150,250)
        x = pred.load_model_and_pred(model_name = 'model200.pickle',rating = 0.95, wins = 6, time_diff = diff)
        x= str(x[0])
        db.child("users").child("advocate").child(adv).update({"credit score":x})

    return HttpResponse(status=204)

def case_close(request):

    cases = dict(db.child("cases").get().val())
    caseid = request.GET.get("caseid")
    uid = cases[caseid]["uid"]
    timestamp = int(datetime.timestamp(datetime.now()))
    db.child("users").child("users").child(uid).child("cases").child(caseid).child("events").update({timestamp:"case closed"})
    db.child("cases").child(caseid).update({"status":"case closed"})
    db.child("cases").child("users").child(uid).child("cases").child(caseid).update({"epoch":timestamp})
    all =True
    return HttpResponse(json.dumps(all),content_type="json/application")
