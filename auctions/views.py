from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse

from .models import User, auctions, watchlist, Bids, Comments
from .form import new_listing_form, submit_bid_form, comment_form

from django.contrib.auth.decorators import login_required


def index(request):
    all_listing = auctions.objects.filter(closed=False)
    return render(request, "auctions/index.html",{
        'Listings' : all_listing
    })

def all_listening_vw(request):

    categories = auctions().Categories.choices

    if request.method == 'POST':
        all_listing = auctions.objects.filter(category = request.POST['category'])
        return render(request, "auctions/all_listing.html",{
            'Listings' : all_listing,
            'categories': categories,
            'category_selected': int(request.POST['category'])
        })

    else:
        all_listing = auctions.objects.all()
        return render(request, "auctions/all_listing.html",{
            'Listings' : all_listing,
            'categories': categories
        })


@login_required
def watchlist_view(request):
    all_listing = watchlist.objects.filter(user= request.user)

    return render(request, "auctions/watchlist.html",{
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
def close_listing(request, product_id):

    product = auctions.objects.get(pk = product_id)
    if product.user.id == request.user.id:
        product.closed = True
        product.save()

    return redirect(reverse('product', kwargs={'product_id':product_id} ))

@login_required
def rmwhatlist(request, product_id):
    w = watchlist.objects.filter(product = product_id, user = request.user).delete()

    return redirect(reverse('product', kwargs={'product_id':product_id} ))

def product(request, product_id):
    product = auctions.objects.get(pk = product_id)

    if request.user.is_authenticated:
        
        whatlist = watchlist.objects.filter(user = request.user, product = product)
        if request.method == 'POST':
            form = submit_bid_form(request.POST)
            
            if form.is_valid():

                if product.bids.last():
                    last_bid = product.bids.last().bid
                else:
                    last_bid = product.start_bit

                if form.cleaned_data['bid'] > last_bid:

                    a = Bids(bid = form.cleaned_data['bid'], product = product, user = request.user)
                    a.save()
                else:
                    return render(request, "auctions/product.html",{
                            'product' : product,
                            'whatlist' : whatlist,
                            'form' : submit_bid_form(),
                            'msg_error' : 'Bid submited is smaller than the currently one or smaller than the minimum bid',
                            'comment_form': comment_form()
                    })
                    

        
        return render(request, "auctions/product.html",{
        'product' : product,
        'whatlist' : whatlist,
        'form' : submit_bid_form(),
        'comment_form': comment_form()
    })

    return render(request, "auctions/product.html",{
        'product' : product
    })

def comment_endpoint(request, product_id):

    product = auctions.objects.get(pk = product_id)
    c = Comments( product =  product, user = request.user, comment = request.POST['comment'])
    c.save()

    return redirect(reverse('product', kwargs={'product_id':product_id} ))


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
