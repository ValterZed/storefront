from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
import json
import os

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def say_hello(request):
    return render(request,"hello.html", {"name": "VAlter"})

def render_home(request):
    ip = get_client_ip(request)
    with open(r"playground\data\users.json", "r+") as json_file:
        users = json.loads(json_file.read())
    
    if ip not in users.keys():
        users[ip] = {"name": False}
    
    if users[str(ip)]["name"]:
        loggedInWithName = True
    else:
        loggedInWithName = False

    with open(r"playground\data\users.json", "w+") as json_file:
        json_file.write(json.dumps(users))

    return render(request,"home.html", {"LoggedInWithName": loggedInWithName},)

def logged_in(request):
    ip = get_client_ip(request)
    
    with open(r"playground\data\users.json", "r+") as json_file:
        print(json_file)
        users = json.loads(json_file.read())


    users[str(ip)]["name"] == request.GET.get("", False)
    print(users[str(ip)]["name"])
    
    with open(r"playground\data\users.json", "w+") as json_file:
        json_file.write(json.dumps(users))
    
    return render(request, "redirect.html", {"link": "/f/"})

def generate(request):
    a = (request.POST.get("query"))
    return render(request,"home.html",  RequestContext(request))
