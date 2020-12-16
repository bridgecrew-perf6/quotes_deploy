from __future__ import unicode_literals
from django.db import models
from time import gmtime, strftime
import re
import bcrypt

class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must include two characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must include two characters."
        if postData['birthday'] == strftime("%Y-%m-%d"):
            errors['birthday'] = "Birthday must be in the past."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Email address is not valid.")
        new_user = Users.objects.filter(email=postData['email'])
        if len(new_user) > 0:
            errors['email'] = ("Email is already in use.")
        if len(postData['password']) < 8:
            errors['password'] = "Password must include eight characters."
        if postData['password_confirm'] != postData['password']:
            errors['password_confirm'] = "Passwords must match."
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Email address is not valid.")
        login_user = Users.objects.filter(email=postData['email'])
        if len(login_user) == 0:
            errors['email'] = ("User email not found.")
        return errors
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

class QuotesManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 2:
            errors['quoted_by'] = "Quote Author must be at least two characters."
        if len(postData['message']) < 10:
            errors['message'] = "Message must be at least ten characters."
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birthday = models.DateField(null=True)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=100)
    password_confirm = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Quotes(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.TextField()
    uploaded_by = models.ForeignKey(Users, related_name="quotes_uploaded", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(Users, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuotesManager()

