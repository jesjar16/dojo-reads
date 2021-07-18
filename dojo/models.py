from django.db import models
from datetime import datetime, timedelta
from calendar import isleap
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking name
        if len(postData['name']) == 0:
            errors['name_emp'] = "Name can not be empty"
        elif len(postData['name']) > 0 and len(postData['name']) < 2:
            errors['name_len'] = "First name should be less at least 2 characters long"
            
        # checking alias
        if len(postData['alias']) == 0:
            errors['alias_emp'] = "Alias can not be empty"
        elif len(postData['alias']) > 0 and len(postData['alias']) < 2:
            errors['alias_len'] = "Alias should be less at least 2 characters long"
                
        # checking valid email 
        if len(postData['email']) == 0:
            errors['email_emp'] = "Email address can not be empty"
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']):    # testing if field matches pattern        
                errors['email_val'] = "Email address is invalid" 
        
        # checking password    
        if len(postData['password']) == 0:
            errors['password_emp'] = "Password can not be empty"
        elif len(postData['password']) < 8:
            errors['password_len'] = "Password should be less at least 8 characters long"                
        
        # checking password 2   
        if len(postData['password2']) == 0:
            errors['password2_emp'] = "Password confirmation can not be empty"
        elif len(postData['password2']) < 8:
            errors['password2_len'] = "Password confirmation should be less at least 8 characters long"    
            
        # checking password 1 and 2
        if len(postData['password']) > 7 and len(postData['password2']) > 7:
            if postData['password'] != postData['password2']:    
                errors['password_dif'] = "Passwords do not match, please try again"

        return errors
    
    def basic_validator2(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking valid email 
        if len(postData['email_login']) == 0:
            errors['email_login_emp'] = "Email address can not be empty"
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email_login']):    # testing if field matches pattern        
                errors['email_login_val'] = "Email address is invalid"
                
        # checking password    
        if len(postData['password_login']) == 0:
            errors['password_login_emp'] = "Password can not be empty"
        elif len(postData['password_login']) < 8:
            errors['password_login_len'] = "Password should be less at least 8 characters long"
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)    
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # reviewed = a list of books a given user has reviewed
    # user_books = a list of books reviewed by a user
    # review = a review made by a user
    objects = UserManager()

    def __repr__(self):
        return f"User: (ID: {self.id}) -> {self.first_name} {self.last_name} by {self.email}"
    
# new models for dojo reads app

class AuthorManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking author
        if len(postData['author']) == 0 and postData['author_lst'] == '-':
            errors['author_emp'] = "Please select an author from the list or add a new one"
            
        if len(postData['author']) != 0 and postData['author_lst'] != '-':
            errors['author_mul'] = "Please either select an author from the list or add a new one, but not both"            
                    
        return errors

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # books = a list of books associated with a given author
    objects = AuthorManager()

    def __repr__(self):
        return f"Author: (ID: {self.id}) -> {self.title}"

class BookManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking first name
        if len(postData['title']) == 0:
            errors['title_emp'] = "Title can not be empty"
            
        if len(postData['title']) < 2:
            errors['title_len'] = "Title must be at least 2 characters"            
                    
        return errors
        
class Book(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="reviewed", on_delete=models.CASCADE) # the user who reviewed a given book
    users = models.ManyToManyField(User, related_name="user_books") # a list of users who have reviewed a given book
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE) # the user who reviewed a given book
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # review_detail = a review for a given user
    objects = BookManager()

    def __repr__(self):
        return f"Book: (ID: {self.id}) -> {self.title}"    

class ReviewManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking review
        if len(postData['review']) == 0:
            errors['review_emp'] = "Review can not be empty"
            
        if len(postData['review']) < 10:
            errors['review_len'] = "Review must be at least 10 characters"            
            
        # checking rating
        if len(postData['rating']) == 0:
            errors['rating_emp'] = "Rating can not be empty"
            
        if postData['rating'] < "1" or postData['rating'] > "5":
            errors['rating_ran'] = "Rating must be between 1 and 5"
                    
        return errors
        
class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="review", on_delete=models.CASCADE) # the user who reviewed a given book
    book = models.ForeignKey(Book, related_name="review_detail", on_delete=models.CASCADE) # the book which got a review
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

    def __repr__(self):
        return f"Review: (ID: {self.id}) -> {self.review}"    
    
