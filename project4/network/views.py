from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import datetime
from .models import User, Post
from django.http import JsonResponse


def index(request):
    posts = Post.objects.all().order_by('time').reverse()
    p = Paginator(posts, 10)
    page = request.GET.get("page")
    pst = p.get_page(page)
    return render(request, "network/index.html", {
        "posts":pst
    })

def profile(request, name):
    u = User.objects.get(username = name)
    t = False
    if request.user.is_authenticated:
        t = request.user.follow.filter(username = name).exists()
    if request.method == "POST":
        if t:
            request.user.follow.remove(u)
            t = False
        else:
            request.user.follow.add(u)
            t = True
    p = u.Posts.all().order_by('time').reverse()
    pag = Paginator(p, 10)
    page = request.GET.get("page")
    pst = pag.get_page(page)
    return render(request, "network/profile.html", {
        "User" : u,
        "followed" : t,
        "followers" : u.followers.all().count(),
        "posts" : pst,
        "followings" : u.follow.all().count()
    })

def edit(request, id):
        p = Post.objects.get(id = id)
        if p.user.username != request.user.username:
            return HttpResponseRedirect(reverse("index"))
        
        if request.method == "POST":
            con = request.POST["edit"]
           
            
            p.content = con
            
            p.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, "network/edit.html",{
            'p' : p
        })
def like_post(request, post_id):
    post = Post.objects.get(id = post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    print("hihohoh", liked)
    return JsonResponse({'liked': liked})
def post(request):
    if request.method == "POST":
        print("hi")
        con = request.POST["newpost"]
        p = Post(user = request.user, content = con, time = datetime.datetime.now())
        print(con)
        p.save()
        return HttpResponseRedirect(reverse('index'))

def following(request):
    if request.user.is_authenticated:
        
        f = request.user.follow.all()
        p = []
        posts = Post.objects.all().order_by('time').reverse()
        for post in posts:
            if post.user in f:
                p.append(post)
        pag = Paginator(p, 10)
        page = request.GET.get("page")
        pst = pag.get_page(page)
        return render(request, "network/following.html", {
            "posts" : pst
        })
    return HttpResponseRedirect(reverse("index"))
    
    
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

