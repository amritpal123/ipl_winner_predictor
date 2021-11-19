from django.shortcuts import render, redirect

import matplotlib.pyplot as mlt; mlt.rcdefaults()
import seaborn as sns

import pandas as pd

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login,logout,authenticate

from .signupform import SignUpForm

from django.contrib import  messages

user=None

matches = pd.read_csv('matches.csv')
matches['winner'].fillna('Draw', inplace=True)

matches.replace(
    ['Mumbai Indians', 'Kolkata Knight Riders', 'Royal Challengers Bangalore', 'Deccan Chargers', 'Chennai Super Kings',
     'Rajasthan Royals', 'Delhi Daredevils', 'Gujarat Lions', 'Kings XI Punjab',
     'Sunrisers Hyderabad', 'Rising Pune Supergiant', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Delhi Capitals']
    , ['MI', 'KKR', 'RCB', 'DC', 'CSK', 'RR', 'DD', 'GL', 'KXIP', 'SRH', 'RPS', 'KTK', 'PW', 'DD'], inplace=True)


from .ipl import predict_winner

mlt.style.use('fivethirtyeight')

def index(request):
    global user
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

    except:
        pass

    if user is not None:
        return render(request, 'home.html')

    else:
        return redirect("/")

def dash(request):
    return render(request, 'dash.html')

def a(request):
    mlt.subplots(figsize=(10,7))
    sns.countplot(x='season', hue='toss_decision', data=matches)
    mlt.savefig("static/image.png", format='png')
    return render(request, 'show.html')

def d(request):
    mlt.subplots(figsize=(12, 6))
    sns.countplot(x='season', data=matches, palette=sns.color_palette('winter'))

    mlt.savefig("static/image.png", format='png')
    return render(request, 'show.html')


def i(request):
    mlt.subplots(figsize=(10,12))

    ax = matches['player_of_match'].value_counts().head(10).plot.bar(width=.8, color=sns.color_palette('inferno',
                                                                                                       10))
    ax.set_xlabel('player_of_match')
    ax.set_ylabel('count')
    for p in ax.patches:
        ax.annotate(format(p.get_height()), (p.get_x() + 0.15, p.get_height() + 0.25))

    mlt.savefig("static/image.png", format='png')
    return render(request, 'show.html')

def target(request):
    if request.method == "POST":

        test={}

        test['team1']=request.POST.get('team1')
        test['team2'] = request.POST.get('team2')
        test['venue'] = request.POST.get('venue')

        test['toss_winner'] = request.POST.get('tosswin')
        test['toss_decision'] = request.POST.get('tossd')

        if test['team1']!= test['team2']:
            out = predict_winner(test)
            print(out)

            data = {'output': out}

        else:
            data = {'output': ""}
            messages.error(request,"Same team selected")

        if test['toss_winner'] == test['team2'] or test['toss_winner'] == test['team1']:
            out = predict_winner(test)
            print(out)

            data = {'output': out}

        else:
            data = {'output': ""}
            messages.error(request,"Select appropraite team in toss winner")

    else:
        data = {'output': ""}

    return render(request,'target.html',data)

def signup(request):

    if request.method=="POST":

        form=SignUpForm(request.POST)

        if form.is_valid():
            user=form.save()

            """login(request,user)"""
            messages.success(request,"Successfully Sign up")
            return redirect("/")
        else:
            print('error')

            for msg in form.error_messages:
                messages.error(request,f'{form.error_messages[msg]}')

    form =SignUpForm()
    return render(request,'signup.html',context={'form':form})

def logout_request(request):

    global user

    logout(request)
    user=None
    return redirect("/")

def login(request):

    return render(request,"Login.html")