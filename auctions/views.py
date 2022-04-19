from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse

from .models import User, auctions, watchlist
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

@login_required
def addwhatlist(request, product_id):

    product = auctions.objects.get(pk = product_id)
    w = watchlist(product = product, user = request.user)
    w.save()

    return redirect(reverse('product', kwargs={'product_id':product_id} ))

@login_required
def rmwhatlist(request, product_id):
    w = watchlist.objects.filter(product = product_id, user = request.user).delete()

    return redirect(reverse('product', kwargs={'product_id':product_id} ))

def product(request, product_id):
    product = auctions.objects.get(pk = product_id)

    if request.user.is_authenticated:
        whatlist = watchlist.objects.filter(user = request.user, product = product)
        
        if whatlist:
            return render(request, "auctions/product.html",{
            'product' : product,
            'whatlist' : whatlist
    })

    return render(request, "auctions/product.html",{
        'product' : product,
        'whatlist' : False
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
