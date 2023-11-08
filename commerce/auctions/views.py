from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_Listings, Categories, Commenst, Bids


def index(request):
    listings = Auction_Listings.objects.filter(is_open = True)
    return render(request, "auctions/index.html",{
        "active" : listings
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
def createNew(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            bid = Bids.objects.create(price = request.POST["bid"], user = request.user)
            
            listing = Auction_Listings(
                title = request.POST["title"],
                description = request.POST["description"],
                is_open = True,
                user = request.user,
                image_link = request.POST["image"],
                biding = bid
            )
            
            if request.POST["category"] != "":
                cats = Categories.objects.all()
                flag = False
                for c in cats:
                    if c.cat == request.POST["category"]:
                        flag = True
                        break
                if not flag:
                    cat = Categories(
                        cat = request.POST["category"]
                    )
                    cat.save()
                else:
                    cat = c
                listing.category = cat
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html")
    else:
        return HttpResponseRedirect(reverse("index"))

def listing(request, title):
    try:
        item = Auction_Listings.objects.get(title = title)
    except:
        return render(request, "auctions/error.html")
    if item:
        w = False

        if request.user in item.users.all():
            
            w = True
        else:
            w = False
        b = request.user.is_authenticated
        return render(request, "auctions/item.html",{
            "item" : item,
            "w" : w,
            "b" : b,
            "c" : item.comments.all()
        })

    
def addTowatchlist(request, title):
    try:
        item = Auction_Listings.objects.get(title = title)
    except:
        return render(request, "auctions/error.html")
    w = True
    if request.method == "POST":   
        if request.user in item.users.all():
            w = False
            request.user.watchlist.remove(item)
        else:
            request.user.watchlist.add(item)
            w = True
    return HttpResponseRedirect(reverse("title", args=[item.title]))
def watchlist(request):
    if request.user.is_authenticated:
        w = request.user.watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "watch" : w
        })
    else:
        return HttpResponseRedirect(reverse("index"))

def place_bid(request, title):
    if request.user.is_authenticated:
        try:
            item = Auction_Listings.objects.get(title = title)
        except:
            return render(request, "auctions/error.html",
                          {
                              "msg" : "Item not found"
                          })
        if request.method == "POST":
            update = int(request.POST["bid"])
            if  update > item.biding.price:
            
                item.biding.price = update
                item.biding.user = request.user
                item.biding.save()
                item.save()
            else:
                return render(request, "auctions/error.html",{
                    "msg" : "BID TOO LOW TRY AGAIN" 
                })
    return HttpResponseRedirect(reverse("title", args=[item.title]))
def close(request, title):
    item = Auction_Listings.objects.get(title = title)
    if request.user.is_authenticated and item.user == request.user:
        item.is_open = False
        item.save()
    return HttpResponseRedirect(reverse("index"))
def comment(request, title):
    itemu = Auction_Listings.objects.get(title = title)
    if request.user.is_authenticated:
        if request.method == "POST":
            c = Commenst(comment = request.POST["comment"], user = request.user, item = itemu)
            c.save()
    return HttpResponseRedirect(reverse("title", args=[itemu.title]))

def categories(request):
    c = Categories.objects.all()
    print(c)
    print("HIIIII")
    return render(request, "auctions/categories.html",{
        "categ" : c
    })
def category_items(request, id):
    print("lololololololoo",id)
    cat = Categories.objects.get(id = id)
    print(cat)
    items = cat.lists.all()
    print(items)
    print("lololololol")
    return render(request,"auctions/category_items.html", {
        "category" : cat.cat,
        "items" : items
    })
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return render(request, "auctions/error.html", {
            "msg" : "No Profile exists for this name"
        })
    l = Auction_Listings.objects.filter(user = user)
    return render(request, "auctions/profile.html", {
        "name" : username,
        "items" : l
    })
def like(request, id, name):
    user = User.objects.get(username = name)
    comment = Commenst.objects.get(id = id)
    if user in comment.likedBy.all():
        comment.likes = comment.likes - 1
        comment.likedBy.remove(user)
        comment.save()
    else:
        comment.likes = comment.likes + 1
        comment.likedBy.add(user)
        print(comment.likedBy.all())
        comment.save()
        print("jdfljdsfkldjf", comment.likes)
    return HttpResponseRedirect(reverse("title", args=[comment.item.title]))

