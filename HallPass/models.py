from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
	def registration_validator(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(postData['fname']) < 1:
			errors['first_name'] = "First name must be at least 1 character"
		if len(postData['lname']) < 1:
			errors['last_name'] = "Last name must be at least 1 character"
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Invalid email address"
		if len(postData['password']) < 8:
			errors['password'] = "Password must be at least 8 characters"
		if postData['password_confirm'] != postData['password']:
			errors['password_confirm'] = "Password confirmation does not match password"
		return errors

	def login_validator(self, postData):
		errors = {}
		user = User.objects.filter(email=postData['email'])
		if not user:
			errors['email'] = "This email address does not exist in our records"
		else:
			user0 = user[0]
			if not bcrypt.checkpw(postData['password'].encode(), user0.password.encode()):
				errors['password'] = "Invalid password"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()


class CelebManager(models.Manager):
    def celebvalidator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name must be at least 3 characters"
        if len(postData['comments']) < 3:
            errors['comments'] = "Comments field must have at least 3 characters"
        return errors

class Celeb(models.Model):
	ranking = models.PositiveSmallIntegerField()
	photo = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	comments = models.TextField()
	users = models.ManyToManyField(User, related_name="celebs")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = CelebManager()