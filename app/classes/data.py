# This is where all the database collections are defined. A collection is a place to hold a defined 
# set of data like Users, Blogs, Comments. Collections are defined below as classes. Each class name is 
# the name of the data collection and each item is a data 'field' that stores a piece of data.  Data 
# fields have types like IntField, StringField etc.  This uses the Mongoengine Python Library. When 
# you interact with the data you are creating an onject that is an instance of the class.
import random
from sys import getprofile
from tokenize import String
from typing import KeysView
from xmlrpc.client import Boolean
from dataclasses import dataclass
from setuptools import SetuptoolsDeprecationWarning
from app import app
from flask import flash, redirect
from flask_login import UserMixin, current_user
from mongoengine import Document, ListField, FileField, EmailField, StringField, IntField, ReferenceField, DateTimeField, BooleanField, FloatField, CASCADE
import datetime as dt
import jwt
from time import time
from bson.objectid import ObjectId
from flask_security import RoleMixin
from functools import wraps


class User(UserMixin, Document):
    createdate = DateTimeField(defaultdefault=dt.datetime.utcnow)
    gid = StringField(sparse=True, unique=True)
    gname = StringField()
    gprofile_pic = StringField()
    username = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField()
    image = FileField()
    prononuns = StringField()
    role = StringField()
    meta = {
        'ordering': ['lname','fname']
    }

class Blog(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    subject = StringField()
    content = StringField()
    tag = StringField()
    num = IntField()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }
class Listing(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    gym_location = StringField()
    gym_picture = FileField()
    gym_quality = StringField()
    price = StringField()
    gym_contact = EmailField()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }
class Comment(Document):
    # Line 63 is a way to access all the information in Course and Teacher w/o storing it in this class
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    blog = ReferenceField('Blog',reverse_delete_rule=CASCADE)
    # This could be used to allow comments on comments
    comment = ReferenceField('Comment',reverse_delete_rule=CASCADE)
    # Line 68 is where you store all the info you need but won't find in the Course and Teacher Object
    content = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Clinic(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()
    name = StringField()
    streetAddress = StringField()
    city = StringField()
    state = StringField()
    zipcode = StringField()
    description = StringField()
    lat = FloatField()
    lon = FloatField()
    
    meta = {
        'ordering': ['-createdate']
    }

class Review(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    name = StringField()
    subject = StringField()
    text = StringField()
    rating = IntField()
    subject = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Reply(Document):
    # Line 63 is a way to access all the information in Course and Teacher w/o storing it in this class
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    review = ReferenceField('Review',reverse_delete_rule=CASCADE)
    name = StringField()
    # This could be used to allow comments on comments
    outer = BooleanField()
    replies = ListField()
    dFromOuter = IntField()
    #ReferenceField('Reply',reverse_delete_rule=CASCADE)
    # Line 68 is where you store all the info you need but won't find in the Course and Teacher Object
    text = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class League(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    name = StringField()
    sport = StringField()
    founder = StringField()
    num_of_teams = IntField()
    address = StringField ()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }
