from django.http import HttpResponse
from django.shortcuts import render
from . import util
import markdown2
import re
from  .form import InputForm, ModifyForm
from random import randrange

from . import util


def index(request):
    search = request.GET.get('q')
    if search is None:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        entries = util.list_entries()
        r = re.compile(".*"+search+".*", re.IGNORECASE)
        newlist = list(filter(r.match, entries)) # Read Note below
        return render(request, "encyclopedia/index.html", {
            "entries": newlist
        })
        

def test(request):
    return HttpResponse("hello testing")

def page(request, page):
    list_entries= util.list_entries()
    entry=util.get_entry(page)
    html_string = markdown2.markdown(entry)
    #return HttpResponse(f"{html_string}")
    return render(request, "encyclopedia/entry.html", {
        "entry": html_string, "id": page
    })

def add(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = InputForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            bodyT = "# " + form['title'].value() +"\n" + form['body'].value()
            #util.save_entry(form['title'].value(),form['body'].value())
            util.save_entry(form['title'].value(),bodyT)
            return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

    # if a GET (or any other method) we'll create a blank form
    else:
        form =  InputForm

    return render(request, "encyclopedia/add.html", {"form": form})


def modify(request, id):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = InputForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            bodyT = "# " + form['title'].value() +"\n" + form['body'].value()
            #util.save_entry(form['title'].value(),form['body'].value())
            util.save_entry(form['title'].value(),bodyT)
            return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
         

    # if a GET (or any other method) we'll create a blank form
    else:
        entry=util.get_entry(id)
        
        data = {'title': id, 'body': entry.replace("# "+id, "")}
        form =  ModifyForm(data)
        
       # form.fields["title"].initial=entry.title       # form.body=entry.content
    return render(request, "encyclopedia/modify.html", {"form": form, "id": id})


def random(request):
    entries = util.list_entries()
    page = entries[randrange(len(entries))]
    entry=util.get_entry(page)
    html_string = markdown2.markdown(entry)
    #return HttpResponse(f"{html_string}")
    return render(request, "encyclopedia/entry.html", {
        "entry": html_string, "id": page
    })
    

def search(request):
    entries = util.list_entries()
    r = re.compile(".*r*")
    newlist = list(filter(r.match, entries)) # Read Note below
    return HttpResponse(f"{newlist}")
