from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel, DealerReview, ReviewPost
from .restapis import get_dealers_from_cf, get_request, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
import logging
import json


print()
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Views

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
    

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password"
            return render(request, 'djangoapp/login', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")        
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "The user already exists.")
            return redirect('djangoapp:registration')


#Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/98f9f7ac-eac8-4b14-8a1b-f707b7642a8b/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        print(dealerships)
        return render(request, 'djangoapp/index.html', context)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://eu-de.functions.appdomain.cloud/api/v1/web/98f9f7ac-eac8-4b14-8a1b-f707b7642a8b/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id= id)
        context["dealer"] = dealer
        print("1")
    
        review_url = "https://eu-de.functions.appdomain.cloud/api/v1/web/98f9f7ac-eac8-4b14-8a1b-f707b7642a8b/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, id= id)  
        context["reviews"] = reviews
        print("2")

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
#@login_required add at the end to have backed check for authentication
def add_review(request, id):
    context = {}
    dealer_url = "https://eu-de.functions.appdomain.cloud/api/v1/web/98f9f7ac-eac8-4b14-8a1b-f707b7642a8b/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id= id)
    context["dealer"] = dealer

    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.car_make.name  
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year)

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://eu-de.functions.appdomain.cloud/api/v1/web/98f9f7ac-eac8-4b14-8a1b-f707b7642a8b/dealership-package/post-review"
            post_request(review_post_url, new_payload, id= id)

        return redirect("djangoapp:dealer_details", id= id)

