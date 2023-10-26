from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q, Max
from datetime import date
from decimal import Decimal
from  .form import BidForm, AddForm

from .models import User, Product, Auction, Watchlist, Comment


def index(request):
            product_list = Product.objects.all()
             
            for product in product_list:
                auction_bid = Auction.objects.select_related().filter()
               
           # return HttpResponseRedirect(reverse("index"))
            return render(request, "auctions/index.html", {
                "product_list": product_list, "auction_bid": auction_bid, "user": request.user
            })
  


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            # success 
            login(request, user)
            product_list = Product.objects.all()
             
            for product in product_list:
                auction_bid = Auction.objects.select_related().filter()
               
           # return HttpResponseRedirect(reverse("index"))
            return render(request, "auctions/index.html", {
                "product_list": product_list, "auction_bid": auction_bid, "user": user
            })
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

def bid(request,id):
    product_detail = Product.objects.filter(id=id, product_owner=request.user)
    max_bid_model = Auction.objects.filter(product_sold=product_detail.first(),winning_bid=True ).first() 
    if not max_bid_model:
         max_bid = "na"
         bid_id="na"
    else:
         max_bid =  getattr(max_bid_model, "amount_bid")
         bid_id =  getattr(max_bid_model, "id")

    if product_detail: 
        return render(request, "auctions/product_owner.html", {
                "product_detail": product_detail ,  "error":"no", "max_bid" : max_bid, "bid_id": bid_id
            })

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = BidForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            id_temp = request.POST["id"]
            bid = form.cleaned_data["bid"]
            product_detail = Product.objects.filter(id=id_temp) 
            product_bid_high = Product.objects.filter(id=id_temp,product_starting_bid__gte=bid) #check product starting price
            auction_bid_high = Auction.objects.filter(product_sold=product_detail.first(),amount_bid__gte=bid) #
            if not product_bid_high and not auction_bid_high:
                    looser_bid_tmp=Auction.objects.all()
                    looser_bid = looser_bid_tmp.filter(product_sold=product_detail.first())  #retrive all bids on product
                    for auction in looser_bid:
                         auction.winning_bid = False 
                         auction.save(update_fields=["winning_bid"]) 
                    bid_details= Auction(product_sold=product_detail.first(), user_bid=request.user,amount_bid=bid, winning_bid=True)
                    bid_details.save()    

                    return render(request, "auctions/bid.html", {
                "product_detail": product_detail , "form": form, "error": "Bid Accepted"
                 })
            else:
                                return render(request, "auctions/bid.html", {
                "product_detail": product_detail , "form": form, "error": "bid rejected"
                 })
      
    # if a GET (or any other method) we'll create a blank form
    else:
        form =  BidForm()
    
    product_detail = Product.objects.filter(id=id)
    return render(request, "auctions/bid.html", {
                "product_detail": product_detail , "form": form,"error":"no"
            })

def open_listing(request, id):
    product_detail = Product.objects.filter(id=id, product_owner=request.user)
    if not product_detail: 
         bid(request, id)
    else:
         return render(request, "auctions/product_owner.html", {
                "product_detail": product_detail ,  "error":"no"
            })
         
    
def accept_bid(request,id):
      if request.method == "POST":
        #username = request.POST["username"]
        #product_id = request.POST["id"]
        bid_id = request.POST["bid_id"] 
        product_detail = Product.objects.filter(id=id)
       # product_update = product_detail.first()   
        max_bid_model = Auction.objects.filter(id=bid_id,winning_bid=True).get() 
        #max_bid =  getattr(max_bid_model, "amount_bid")                     
        max_bid= max_bid_model.amount_bid
       # product_update.product_status = "sold" 
        #product_update.product_price = max_bid
        #roduct_update.date_sold=date.today()
        #product_update.save()

        Product.objects.filter(id=id).update(product_status="sold",date_sold=date.today() ,product_price=max_bid)


        bids = Auction.objects.filter(product_sold=Product.objects.filter(id=id).first())  #retrive all bids on product
        for auction in bids:
                auction.status_bid = "inactive" 
                auction.save(update_fields=["status_bid"]) 

        #product_update.save(update_fields=["product_status", "date_sold","product_price"]) 
         
        return render(request, "auctions/product_owner.html", {
                "product_detail": product_detail ,  "accepted_bid":"true" ,  "error":bid_id, "tot":max_bid
            
            })
      
def add(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
            form = AddForm(request.POST)
        # check whether it's valid:
            if form.is_valid():
                prod = Product(product_owner=request.user,product_name=form.cleaned_data['product_name'],
                               product_description=form.cleaned_data['product_description'],
                               product_img_url=form.cleaned_data['product_img_url'] ,
                               product_starting_bid=form.cleaned_data['product_starting_bid'])
                prod.save()
                return render(request, "auctions/index.html", {
        "entries": None
    })

    # if a GET (or any other method) we'll create a blank form
    else:
        form =  AddForm()

        return render(request, "auctions/add.html", { "form" : form 
            
            })