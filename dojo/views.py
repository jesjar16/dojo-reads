from django.shortcuts import render, redirect
from django.urls import reverse
from dojo.models import Author, User, Book, Review
from django.contrib import messages
import bcrypt
from django.db import IntegrityError
from dojo.decorators import login_required
from django.db.models import Avg # to calculate average

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    # getting form variables
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    # errors dict is received
    errors = User.objects.basic_validator(request.POST)
    
    # if there are errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        # getting the current form values
        form_data = {
            'name': name,
            'alias': alias,
            'email': email
        }
        
        request.session['form_data'] = form_data
        
        return redirect(reverse("my_index"))
    else:
        try:
            # hashing password
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            # creating the user
            this_user = User.objects.create(name=name, alias=alias, email=email, password=hashed_password) 

            # creating dictionary with user's data
            user_data = {
                    'user_id': this_user.id,
                    'name': this_user.name.capitalize(),
                    'alias': this_user.alias.capitalize(),
                    'email': this_user.email,
                    'action': 'register'
            }
            
            # saving user dictionary to session variable
            request.session['user_data'] = user_data
                
            messages.success(request, "User successfully created and logged in")
        
            return redirect(reverse("my_success"))
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                messages.error(request, 'Email is already registered, try logging in')
                
                # getting the current form values
                form_data = {
                    'name': name.capitalize(),
                    'alias': alias.capitalize(),
                    'email': email
                }
                
                request.session['form_data'] = form_data

            return redirect(reverse("my_index"))

def login(request):
    # form variables are received
    email_login = request.POST['email_login']
    password_login = request.POST['password_login']
    
    # errors dict is received
    errors = User.objects.basic_validator2(request.POST)
    
    # if there are errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        # saving form data into form_data dictionary
        form_data = {
            'email_login': email_login
        }
        
        request.session['form_data'] = form_data
        
        return redirect(reverse("my_index"))
    else: # no errors
        user = User.objects.filter(email=email_login)
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(password_login.encode(), logged_user.password.encode()):
                # creating session variables for logged in user
                user_data = {
                    'user_id': logged_user.id,
                    'name': logged_user.name.capitalize(),
                    'alias': logged_user.alias.capitalize(),
                    'email': logged_user.email,
                    'action': 'login'
                }
                
                request.session['user_data'] = user_data
                
                messages.success(request, "You have successfully login")
                
                return redirect(reverse("my_success"))
            else:
                messages.error(request, "Wrong email or password")
                
                return redirect(reverse("my_index"))
        else:
            messages.error(request, "Wrong email or password")
                
            return redirect(reverse("my_index"))

@login_required
def success(request):
    return redirect(reverse("my_book_review"))
    
@login_required    
def homepage(request):
    return render(request, "homepage.html")

@login_required    
def book_review(request):
    first_3_reviews = Review.objects.all().order_by('-id').annotate(Avg('rating'))[:3:1]
    rest_of_reviews = Review.objects.all().order_by('-id')[3:]
    
    print(first_3_reviews)
    
    context= {
        'first_3_reviews': first_3_reviews,
        'rest_of_reviews': rest_of_reviews
    }
    return render(request, "book_review_home.html", context)

@login_required    
def add_breview(request):
    # getting all authors to populate author select
    all_authors = Author.objects.all()
    
    context = {
        'all_authors': all_authors
    }
    
    return render(request, "add_breview.html", context)

@login_required  
def add(request):
    # form variables are received
    title = request.POST['title']
    author_lst = request.POST['author_lst'] 
    print ("Author LIST ", author_lst)
    author = request.POST['author']
    review = request.POST['review']
    rating = request.POST['rating']
    
    # errors dict is received
    errors = Book.objects.basic_validator(request.POST)
    
    # adding all error dictionaries   
    errors.update(Author.objects.basic_validator(request.POST))
    errors.update(Review.objects.basic_validator(request.POST))
    
    # if there are errors
    if len(errors) > 0:               
        for key, value in errors.items():
            messages.error(request, value) 

        form_data = {
            'title': title,
            'author_lst': int(author_lst),
            'author': author,
            'review': review,
            'rating': rating
        } 
        
        request.session['form_data'] = form_data
    
        return redirect(reverse("my_add_breview"))
    else: # no errors
        id = request.session['user_data']['user_id']
        this_user = User.objects.get(id=id)
        
        if author:
            # saves author
            this_author = Author.objects.create(name=author)
        else:
            this_author = Author.objects.get(id=author_lst)
        
        # saves book
        this_book = Book.objects.create(title=title, user=this_user, author=this_author)
        
        # saves review
        this_review = Review.objects.create(review=review, rating=rating, user=this_user, book=this_book)        
        
        messages.success(request, "Book and Review successfully added")
        
        if 'form_data' in request.session:
            del request.session['form_data']

        #return redirect(reverse("my_book_review"))
        return redirect(reverse("my_book", args=(this_book.id,)))

@login_required  
def add_sm_review(request):
    # getting form variables
    review = request.POST['review']
    rating = request.POST['rating']
    book_id = request.POST['book_id']    
    
    # errors dict is received
    errors = Review.objects.basic_validator(request.POST)
    
    ''' THIS PART VALIDATES IF USER HAS ALREADY REVIEWED THE BOOK, AND PREVENTS THEM FOR REVIEWING AGAIN
    # chequing if current user has already posted a review
    id = request.session['user_data']['user_id']
    this_user = User.objects.get(id=id)
    
    this_book = Book.objects.get(id=book_id)
    reviewed_by_this_user = Review.objects.filter(user=this_user).filter(book=this_book)
    
    if reviewed_by_this_user:
        errors['reviewed'] = "You have already reviewed this book!"
    
    '''
    # if there are errors
    if len(errors) > 0:                
        for key, value in errors.items():
            messages.error(request, value)

        form_data = {
            'review': review,
            'rating': rating
        } 
        
        request.session['form_data'] = form_data

        return redirect(reverse("my_book", args=(book_id,)))
    else: # no errors
        id = request.session['user_data']['user_id']
        this_user = User.objects.get(id=id)
        
        this_book = Book.objects.get(id=book_id)
        
        # saves review
        this_review = Review.objects.create(review=review, rating=rating, user=this_user, book=this_book)        
        
        messages.success(request, "Review successfully added")
        
        if 'form_data' in request.session:
            del request.session['form_data']

        return redirect(reverse("my_book", args=(book_id,)))
    
@login_required      
def users(request, user_id):
    this_user = User.objects.get(id=user_id)
    
    # getting all reviews by the current user, order descending
    user_reviews = Review.objects.filter(user=this_user).order_by('-id')
    
    # getting the amount of reviews by current user
    total_reviews = Review.objects.filter(user=this_user).count()
        
    context = {
        'user_reviews': user_reviews,
        'total_reviews': total_reviews,
        'this_user': this_user
    }
    
    return render(request, "book_user.html", context)

@login_required    
def book(request, book_id):
    id = request.session['user_data']['user_id']
    this_user = User.objects.get(id=id)
    
    # getting current book
    this_book = Book.objects.get(id=book_id)
    
    # getting all reviews for book
    all_book_reviews = Review.objects.filter(book=this_book).order_by('-id')
    
    context = {
        'this_book': this_book,
        'all_book_reviews': all_book_reviews,
        'this_user': this_user
    }
    return render(request, "book.html", context)    

@login_required    
def del_breview(request):
    # getting form variables
    reviewId = request.POST['reviewId']
    book_id = request.POST['book_id']
    
    # creating review object to delete
    review_to_delete = Review.objects.get(id=reviewId)
    
    # deleting review
    review_to_delete.delete()
    
    return redirect(reverse("my_book", args=(book_id,)))

@login_required
def about(request):
    return render(request, "about.html")

def logout(request):
    # deleting session variables
    if 'form_data' in request.session:
        del request.session['form_data']
        
    if 'user_data' in request.session:
        del request.session['user_data']
        messages.success(request, "You have successfully logout")
    
    return redirect(reverse("my_index")) 