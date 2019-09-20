from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):        
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME = re.compile(r'^[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        if not NAME.match(postData['first_name']) or len(postData['first_name']) < 2:
            errors["first_name"] = "Invalid First name"
        if not NAME.match(postData['last_name']) or len(postData['last_name']) < 2:
            errors["last_name"] = "Invalid Last name"
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 10:    # test whether a field matches the pattern            
            errors['email_invalid'] = "Invalid email address!"
        if len(postData['password']) < 8 or postData['password']!=postData['confirm_password']:
            errors["password"] = "Invalid password/Password doesn't match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 10:    # test whether a field matches the pattern            
            errors['email_invalid'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Invalid password/email"
        return errors

    def job_validator(self, postData):
        errors = {}
        NAME = re.compile(r'^[a-zA-Z]+$')
        if not NAME.match(postData['title']) or len(postData['title']) < 3:
            errors["title"] = "Invalid Title"
        if not NAME.match(postData['description']) or len(postData['description']) < 3:
            errors["description"] = "Invalid description"
        if not NAME.match(postData['location']) or len(postData['location']) < 3:
            errors["location"] = "Invalid location"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()    # add this line!

class Job(models.Model):
	users = models.ManyToManyField(User, related_name = "users_jobs")
	user = models.ForeignKey(User, related_name = "jobs")
	title = models.CharField(max_length = 45)
	description = models.TextField()
	location = models.CharField(max_length = 45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
# Create your models here.
