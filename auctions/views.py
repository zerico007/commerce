from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django import forms
from django.forms import ModelForm
import datetime
from django.contrib import messages


def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
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

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingsForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            f = Listings.objects.all()
            f.title = form.cleaned_data["title"]
            f.description = form.cleaned_data["description"]
            f.starting_price = form.cleaned_data["starting_price"]
            f.listing_photo = form.cleaned_data["listing_photo"]
            f.category = form.cleaned_data["category"]
            listing = form.save(commit=False)
            listing.date_created = datetime.datetime.now()
            listing.listing_user = User.objects.get(id=request.user.id)
            listing.save()
            messages.success(request, "Your listing is now active!")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "message": "Form not valid",
                "form": form
            })
        
    else:
        form = ListingsForm()
        return render(request, "auctions/create.html", {
            "form": form
        })

def listing_page(request, title):
    if request.method == "POST":
        form_b = BidsForm(request.POST, request.user)
        form_c = CommentsForm(request.POST, request.user)

        last_bid = Bids.objects.filter(bid_listing=Listings.objects.get(title=title)).last()
        if last_bid:
            last_bid_price = last_bid.bid_price
        else:
            last_bid_price = (Listings.objects.get(title=title)).starting_price
        if form_b.is_valid():
            bid_amount = form_b.cleaned_data["bid_price"]
            if bid_amount is not None:
                if bid_amount <= last_bid_price:
                    return render(request, "auctions/apology.html", {
                        "message": "Invalid bid. Your bid is lower than or equal to last bid."
                    })
                bid = form_b.save(commit=False)
                bid.bid_user = User.objects.get(id=request.user.id)
                bid.bid_listing = Listings.objects.get(title=title)
                bid.save()
                messages.success(request, "Bid successfully placed!")
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/listing_page.html", {
                "message": "Invalid bid",
                "form_b": form_b,
                "form_c": form_c
            })

        if form_c.is_valid():
            c = form_c.cleaned_data["comment"]
            if c is not None:
                comment = form_c.save(commit=False)
                comment.comment_listing = Listings.objects.get(title=title)
                comment.comment_user = User.objects.get(id=request.user.id)
                comment.save()
                messages.success(request, "Comment successfully posted!")
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/listing_page.html", {
                "message": "Invalid Comment",
                "form_b": form_b,
                "form_c": form_c
            })

    else:
        form_b = BidsForm()
        form_c = CommentsForm()
       
        bid_count = len(Bids.objects.filter(bid_listing=Listings.objects.get(title=title)))
        last_bid = Bids.objects.filter(bid_listing=Listings.objects.get(title=title)).last()
        comments = Comments.objects.filter(comment_listing=Listings.objects.get(title=title))
        
        if last_bid:
            last_bid_user = last_bid.bid_user
        else:
            last_bid_user = None
        return render(request, "auctions/listing_page.html",{
        "listing": Listings.objects.get(title=title),
        "title": Listings.objects.get(title=title),
        "form_b": form_b,
        "form_c": form_c,
        "count": bid_count,
        "last_bid_user": last_bid_user,
        "comments": comments,
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        title = request.POST["listing"]
        watch_listings = Watchlist.objects.filter(watchlist_user=User.objects.get(id=request.user.id))
        for i in watch_listings:
            if i.listing.title == title:
                return render(request, "auctions/watchlist.html", {
                "message": "Already added to watchlist",
                "listings": watch_listings
                })

        w = Watchlist(listing=Listings.objects.get(title=title), watchlist_user=User.objects.get(id=request.user.id))
        w.save()
        messages.success(request, "Added to watchlist!")
        return HttpResponseRedirect(reverse("index"))
    else:
        watch_listings = Watchlist.objects.filter(watchlist_user=User.objects.get(id=request.user.id))
        
        return render(request, "auctions/watchlist.html", {
            "listings": watch_listings
        })

def category(request, category):
    category_listings = Listings.objects.filter(category=category)

    return render(request, "auctions/category.html", {
        "listings": category_listings
    }) 

@login_required
def my_listings(request):
    if request.method == "POST":
        open_title = request.POST.get("open_title", False)
        if open_title:
            listing = Listings.objects.get(title=open_title, listing_user=User.objects.get(id=request.user.id))
            listing.closed = True
            listing.save()
            messages.success(request, "Bid Closed")
            return HttpResponseRedirect(reverse("index"))
        close_title = request.POST.get("close_title", False)
        if close_title:
            listing = Listings.objects.get(title=close_title, listing_user=User.objects.get(id=request.user.id))
            listing.closed = False
            listing.save()
            messages.success(request, "Bid Reopened!")
            return HttpResponseRedirect(reverse("index"))
    else:
        my_listings = Listings.objects.filter(listing_user=User.objects.get(id=request.user.id))
        form = ClosedForm()
        return render(request, "auctions/my_listings.html", {
            "listings": my_listings,
            "form": form
        })
