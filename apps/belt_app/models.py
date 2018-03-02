# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt
from time import gmtime, strftime

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')
PASSWORD_REGEX = re.compile(r'.*[A-Z].*[0-9]')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name should be longer than 2 characters."
        if len(postData['username']) < 2:
            errors["username"] = "Userame should be longer than 2 characters."
        if len(postData['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['match'] = "Your password didn't match."
        if User.objects.filter(username = postData['username']):
            errors['exsists'] = "Username already exists."
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['username']) < 1:
            errors['empty_user'] = "Username is empty."
        if len(postData['password']) < 1:
            errors['empty_pass'] = "Password is empty."
        if not User.objects.filter(username = postData['username']):
            errors['wrong_user'] = "Incorrect Username."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), User.objects.get(username=postData['username']).password.encode()):
                errors['wrong_pass'] = "Incorrect Password."
        return errors

    def trip_validator(self, postData, id):
        errors = {}
        current = strftime("%Y-%m-%d", gmtime())
        print postData['from']
        if len(postData['destination']) < 3:
            errors['short_dest'] = "Destination must be more than 3 characters."
        if len(postData['description']) < 3:
            errors['short_desc'] = "Description must be longer than 3 characters."
        if postData['from'] < current or postData['to'] < postData['from']:
            errors['time_error'] = "The date you provided is incorrect."
        if not errors:
            Trip.objects.create(destination=postData['destination'],description=postData['description'],travel_from=postData['from'],travel_to=postData['to'],my_trip=User.objects.get(id=id))
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager() 

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_from = models.CharField(max_length=255)
    travel_to = models.CharField(max_length=255)
    my_trip = models.ForeignKey(User, related_name="my_trips")
    group_trip = models.ManyToManyField(User, related_name="group_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager() 