from django.db import models

import re

class UserManager(models.Manager): # ⇇ Manager sets up all the conditionals (AKA "if ")
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2: # this is request.POST['first_name']→first_name is key, value is whatever User types in
            errors['first_name'] = "Hey! Your first name must be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Gotta give me something here... at least 2 characters!"
        if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "You gotta enter a valid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Your password has to be at least 8 characters."
        if postData['password'] != postData['confpw']:
            errors['conf_password'] = "Your password and confirm password must match!"
        return errors

    def validate_edit(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2: 
            errors['first_name'] = "Hey! Your first name must be at least 2 characters"
        if len(postData['last_name']) <2:
            errors['last_name'] = "Dude! Gotta have a last name with at least 2 characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "You gotta enter a valid email address!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password  = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} ({self.id})>"

