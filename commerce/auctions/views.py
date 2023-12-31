from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from datetime import date
from decimal import Decimal
from  .form import BidForm, AddForm, CommentForm

from .models import User, Product, Auction, Watchlist, Comment, Category


def index(request):
            product_list = Product.objects.all()
           # user_watch = Watchlist.objects.filter(user_watchlist=request.user).all()
            for product in product_list:
                auction_bid = Auction.objects.select_related().filter()
            if request.user is not None:   
           # return HttpResponseRedirect(reverse("index"))
                return render(request, "auctions/index.html", {
                "product_list": product_list, "auction_bid": auction_bid #, "user": request.user
                    #,                "user_watchlist": user_watch
                 }) 
            else:
                return render(request, "auctions/index.html", {
                "product_list": product_list, "auction_bid": auction_bid 
                 }) 
            
@login_required
def watchlist(request):
            tmp_list= []
            try:
                user_watch_list = Watchlist.objects.filter(user_watchlist=request.user).get()
            except Watchlist.DoesNotExist:
                user_watch_list = None
                return render(request, "auctions/index.html", {
               "watchlist_empty": True , "watchlist_header" : True
            }) 
            except Watchlist.MultipleObjectsReturned:
                 pass 

            user_watch_list = Watchlist.objects.filter(user_watchlist=request.user).all()

            for watch in user_watch_list:
                tmp_list.append(watch.product_watchlist.id) 

            product_list =  Product.objects.filter(pk__in=tmp_list).all()
               
            for product in product_list:
                auction_bid = Auction.objects.select_related().filter()
           # return HttpResponse(f"  {tmp_list} - {product_list[1]} ")
            return render(request, "auctions/index.html", {
               "product_list": product_list, "auction_bid": auction_bid , "watchlist_header" : True
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

@login_required
def bid(request,id):
    product_detail = Product.objects.filter(id=id, product_owner=request.user)
    max_bid_model = Auction.objects.filter(product_sold=product_detail.first(),winning_bid=True ).first() 

    comments = Comment.objects.filter(product_comment=product_detail.first()).all()

    if not max_bid_model:
         max_bid = "na"
         bid_id="na"
    else:
         max_bid =  getattr(max_bid_model, "amount_bid")
         bid_id =  getattr(max_bid_model, "id")

    if product_detail: 
        return render(request, "auctions/product_owner.html", {
                "product_detail": product_detail ,  "error":"no", "max_bid" : max_bid, "bid_id": bid_id, 
                "comments" : comments, "max_bid_model": max_bid_model
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
                "product_detail": product_detail , "form": form, "error": "Bid accepted", 
                "comments" : comments
                 })
            else:
                                return render(request, "auctions/bid.html", {
                "product_detail": product_detail , "form": form, "error": "Bid rejected", 
                "comments" : comments
                 })
      
    # if a GET (or any other method) we'll create a blank form
    else:
        form =  BidForm()
    
    product_detail = Product.objects.filter(id=id)
    comments = Comment.objects.filter(product_comment=product_detail.first()).all()
    return render(request, "auctions/bid.html", {
                "product_detail": product_detail , "form": form,"error":"no", 
                "comments" : comments
            })


@login_required
def open_listing(request, id):
    product_detail = Product.objects.filter(id=id).get()
    comments = Comment.objects.filter(product_comment=product_detail).all()  
    try:
        #watch = Watchlist(user_watchlist=request.user ,product_watchlist=Product.objects.filter(id=id).get())
        watch = Watchlist.objects.filter(product_watchlist=product_detail, user_watchlist=request.user).first()
        bid_tmp = Auction.objects.filter(product_sold=product_detail, winning_bid=True).get()
        max_bid = bid_tmp.amount_bid
    except Auction.DoesNotExist:
        max_bid = 0  
        bid_tmp = None
    except Watchlist.DoesNotExist:
        watch = None
        bid_tmp = None
         
    if request.method == "POST":


        if 'commentform_flag' in request.POST:
            bidform=BidForm()
            commentform=CommentForm(request.POST)
            if commentform.is_valid():
                comment_tmp=Comment(user_comment=request.user, product_comment=product_detail,
                                 comment=commentform.cleaned_data['comment'])
                comment_tmp.save()
                commentform=CommentForm(use_required_attribute=False)
                return render(request, "auctions/open_listing.html", {
                "product_detail": product_detail ,"comments": comments, "bid_details": bid_tmp,
                "bidform": bidform, "commentform":  commentform, "user" : request.user, "watch" : watch
            })
        else: # bid form  submitted         
            bidform=BidForm(request.POST)
            commentform=CommentForm(use_required_attribute=False) 
            bid_result = "aa  %s  " % bidform.is_valid()
           #if bidform.is_valid():  
            actual_bid=bidform.cleaned_data['bid'] #retrive actual bid 
            if  actual_bid > max_bid and actual_bid >= product_detail.product_starting_bid: #actual bid is the winner! #check bid result
                    try:
                        bid_tmp = Auction.objects.filter(product_sold=product_detail, winning_bid=True).all()
                        for auction in bid_tmp:
                            auction.winning_bid = False
                            auction.save(update_fields=["winning_bid"]) 
                    except Auction.DoesNotExist:
                        bid_tmp = None 

                    bid_tmp=Auction(product_sold=product_detail, user_bid=request.user,amount_bid=actual_bid, winning_bid=True)
                    bid_tmp.save()
                    
                    bid_result="Bid inserted correctly." #manage old bids   
            else: 
                    bid_result="your bid is too low"   
            bidform=BidForm()
            try:
                bid_tmp = Auction.objects.filter(product_sold=product_detail, winning_bid=True).get()
                max_bid = bid_tmp.amount_bid

            except Auction.DoesNotExist:
                bid_tmp = None 

            return render(request, "auctions/open_listing.html", {
                "product_detail": product_detail ,  "bid_result":bid_result, "comments": comments,
                "bidform": bidform, "commentform":  commentform, "bid_details": bid_tmp, "user" : request.user, "watch" : watch
            })
    else:
 
        bidform=BidForm()
        commentform=CommentForm(use_required_attribute=False) 
        return render(request, "auctions/open_listing.html", {
                "product_detail": product_detail , "comments": comments,
                "bidform": bidform, "commentform":  commentform, "bid_details": bid_tmp, "user" : request.user, "watch" : watch,
                "pippo" : "pippo"
            })    



         
@login_required    
def accept_bid(request,id): 
    product_detail = Product.objects.filter(id=id).get()
    comments = Comment.objects.filter(product_comment=product_detail).all() 
    try:
        #watch = Watchlist(user_watchlist=request.user ,product_watchlist=Product.objects.filter(id=id).get())
            watch = Watchlist.objects.filter(product_watchlist=product_detail, user_watchlist=request.user).first()
            bid_tmp = Auction.objects.filter(product_sold=product_detail, winning_bid=True).get()
            max_bid = bid_tmp.amount_bid
    except Auction.DoesNotExist:
            max_bid = 0  
            bid_tmp = None
    except Watchlist.DoesNotExist:
            watch = None
            bid_tmp = None

    if request.method == "POST":
        commentform=CommentForm(use_required_attribute=False)
        bid_id = request.POST["bid_id"] 
        prod_id = request.POST["id"]
        try:
            max_bid_model = Auction.objects.filter(id=bid_id,winning_bid=True).get() 
            max_bid= max_bid_model.amount_bid

        except Auction.DoesNotExist:
             return HttpResponse("error, please contact support")
        bidform=BidForm()
        product_detail=Product.objects.filter(id=id).update(product_status="sold",date_sold=date.today() ,product_price=max_bid)
        
        product_detail= Product.objects.filter(id=prod_id).get()
        bids = Auction.objects.filter(product_sold=Product.objects.filter(id=id).first())  #retrive all bids on product
        for auction in bids:
                auction.status_bid = "inactive" 
                auction.save(update_fields=["status_bid"]) 

        return render(request, "auctions/open_listing.html", {
                "product_detail": product_detail , "comments": comments,
                 "bidform": bidform, "commentform":  commentform, "bid_details": max_bid_model, "bid_accepted": True,
                    "user" : request.user, "watch" : watch, "pippo": "pluto"
            })     


@login_required      
def add(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
            form = AddForm(request.POST)
        # check whether it's valid:
            if form.is_valid():
                prod = Product(product_owner=request.user,product_name=form.cleaned_data['product_name'],
                               product_description=form.cleaned_data['product_description'],
                               product_img_url=form.cleaned_data['product_img_url'] ,
                               product_starting_bid=form.cleaned_data['product_starting_bid']
                               )
                prod.save()
                list_cat=form.cleaned_data['product_categories']
                for category in list_cat:
                     categ = Category.objects.filter(category_name=category.category_name).first()
                     prod.product_categories.add(categ)
                     prod.save()
                return render(request, "auctions/index.html", {
        "new_entry": True
    })
        #    else:


         #       return render(request, "auctions/index.html", {
       # "entries": None, "categ": None, "formt": form 
    #})

    # if a GET (or any other method) we'll create a blank form
    else:
        form =  AddForm()

        return render(request, "auctions/add.html", { "form" : form 
            
            })
    
@login_required
def add_watchlist(request, id):
    product_detail = Product.objects.filter(id=id).first()
 
    try:
        watch = Watchlist.objects.filter(product_watchlist=product_detail, user_watchlist=request.user).get()
    except Watchlist.DoesNotExist:
         watch = Watchlist(user_watchlist=request.user ,product_watchlist=product_detail)
         watch.save()
    
    comments = Comment.objects.filter(product_comment=product_detail).all()  
    try:
        bid_tmp = Auction.objects.filter(product_sold=product_detail, winning_bid=True).get()
        max_bid = bid_tmp.amount_bid

    except Auction.DoesNotExist:
        bid_tmp = None  
    
    bidform=BidForm()
    commentform=CommentForm(use_required_attribute=False) 
    return render(request, "auctions/open_listing.html", {
                "product_detail": product_detail , "comments": comments,
                "bidform": bidform, "commentform":  commentform, "bid_details": bid_tmp, "user" : request.user,
                "watch" : watch
            })     


@login_required
def remove_watchlist(request, id):
    product_detail = Product.objects.filter(id=id).get()
    try:
         watch = Watchlist.objects.filter(product_watchlist=product_detail, user_watchlist=request.user).get()
         watch.delete()
         watch = None
    except Watchlist.DoesNotExist:
         watch = None

    comments = Comment.objects.filter(product_comment=product_detail).all()  
    try:
        bid_tmp = Auction.objects.filter(product_sold=product_detail, winning_bid=True).get()
        max_bid = bid_tmp.amount_bid

    except Auction.DoesNotExist:
        bid_tmp = None  

    bidform=BidForm()
    commentform=CommentForm(use_required_attribute=False) 
    return render(request, "auctions/open_listing.html", {
                "product_detail": product_detail , "comments": comments,
                "bidform": bidform, "commentform":  commentform, "bid_details": bid_tmp, "user" : request.user,
                "watch" : watch
            })     

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", { "categories" : categories    
            })

@login_required
def comments(request, id):
    product_detail = Product.objects.filter(id=id)
    comments = Comment.objects.filter(product_comment=product_detail.first()).all()

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            return render(request, "auctions/comments.html", {
        "comments": comments
    })

    # if a GET (or any other method) we'll create a blank form
    else:
        form =  CommentForm()

    return render(request, "auctions/comments.html", {"comments": comments, "form": form})
     