from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse

from .models import User, auctions
from .form import new_listing_form

from django.contrib.auth.decorators import login_required


def index(request):
    all_listing = auctions.objects.all()
    return render(request, "auctions/index.html",{
        'Listings' : all_listing
    })

@login_required
def new_listing(request):

    if request.method == 'POST':
        form = new_listing_form(request.POST)
        if form.is_valid():
            a = auctions(**form.cleaned_data, user=request.user)
            a.save()
            return redirect(reverse('index'))
        
        
        

    return render(request, "auctions/create_listing.html",{
        "form": new_listing_form()
    })

def product(request, product_id):
    listing = auctions.objects.get(product_id)
    print(listing)
    return render(request, "auctions/index.html",{
        'Listing' : listing
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
