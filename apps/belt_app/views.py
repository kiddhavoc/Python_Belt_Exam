# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
    return render(request,'belt_app/index.html', {'everyone':User.objects.all()})


def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Successfully registered!')
            user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()))
            request.session["id"] = user.id
            return redirect('/dashboard')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key,values in errors.iteritems():
                messages.success(request, values)
            return redirect('/')
        else:
            id = User.objects.get(username=request.POST['username']).id
            name = User.objects.get(username=request.POST['username']).name
            request.session['id'] = id
            request.session['name'] = name
        return redirect('/dashboard')
    else:
        messages.error(request, "Create new user!")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def dash(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        context = {
            "user" : User.objects.get(id=request.session['id']).name,
            "my_trips" : Trip.objects.filter(my_trip=user),
            "group_trips" : Trip.objects.filter(group_trip=user),
		    "all_trips" : Trip.objects.exclude(my_trip=user).exclude(group_trip=user)
	    }
        return render(request,'belt_app/dashboard.html', context) 
    else:
        messages.error(request, "Please log in.")
        return redirect('/')


def destination(request, number):
    
    if 'id' in request.session:
        
        context = {
            'trip' : Trip.objects.get(id=number)
        }
        
        return render(request, 'belt_app/destination.html', context)

    else:
        return redirect('/')
   

def add(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        return render(request,'belt_app/add.html')


def process(request):
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST,request.session['id'])
        if len(errors):
            for key,values in errors.iteritems():
                messages.success(request, values)
            return redirect('/add')
        else:
            return redirect('/dashboard')

def join(request,number):
    if 'id' in request.session:
        if Trip.objects.filter(id=number) > 0:
            Trip.objects.get(id=number).group_trip.add(User.objects.get(id=request.session['id']))
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')