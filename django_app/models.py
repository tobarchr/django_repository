from django.db import models
import re

class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_confirmation']:
            errors['password_confirmation'] = "Passwords do not match"
        return errors

    def update_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) ==0:
            errors['first_name'] = "First Name cannot be empty"
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last Name cannot be empty"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['email']) == 0:
            errors['email'] = "Email cannot be empty"
        if postData['email'] == User.objects.filter(email=postData['email']):
            errors['email'] = "Email already exists"
        return errors

    def login_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        return errors

class QouteManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author should be more than 3 characters"
        if len(postData['description']) < 10 and len(postData['description']) > 0:
            errors['description'] = "Qoute should be at more than 10 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Qoute(models.Model):
    author = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(User,related_name="qoutes_uploaded",on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User,related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    objects = QouteManager()