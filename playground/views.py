from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
import os
from django import forms
import openai
from deep_translator import GoogleTranslator


openai.api_key = "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"

rewrite = True

ai_values = {"temperature": 0.7, "max_tokens": 256, "frequency_penalty": 2, "presence_penalty": 0}


def generate(text):
    

    
    prompt = (GoogleTranslator('auto','en').translate(text))

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"write \'{prompt}' in a new way" if rewrite else prompt,
        temperature=ai_values["temperature"],
        max_tokens=ai_values["max_tokens"],
        top_p=1,
        frequency_penalty=ai_values["frequency_penalty"],
        presence_penalty=ai_values["presence_penalty"]
    )

    res = response["choices"][0]["text"]
    svres = (GoogleTranslator('auto','sv').translate(res))


    return svres


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
        with open(f"playground\data\{ip}_history.json", "w+") as json_file:
            dump_dict = {}
            json.dumps(dump_dict)
    
    if users[str(ip)]["name"]:
        loggedInWithName = True
    else:
        loggedInWithName = False

    

    if request.POST.get('query') != None:
        global q
        q = request.POST.get('query')
        return redirect("/rewrite/gen/")



    with open(r"playground\data\users.json", "w+") as json_file:
        json_file.write(json.dumps(users))

    return render(request,"home.html", {"LoggedInWithName": loggedInWithName})

def generating(request):

        ip = get_client_ip(request)
        query = q
        gen_text = generate(query)

        with open(f"playground\data\{ip}_history.json", "r+") as json_file:
            dict = json.loads(json_file.read())
            with open(f"playground\data\{ip}_history.json", "w+") as json_file:
                dict[query] = gen_text
                json_file.write(json.dumps(dict))
        

        return render(request, "display_generated.html", {"generated_text": gen_text})

def generating_fake(request):
    return render(request, "redirect_gen.html")


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

def display_history(request):
    ip = get_client_ip(request)
    input_lst = [""for _ in range(10)]
    value_lst = [""for _ in range(10)]
    with open(f"playground\data\{ip}_history.json", "r+") as json_file:
        dict = json.loads(json_file.read())
    
    for n, item in enumerate(reversed(dict.keys())):
        if n >= 10:
            break
        input_lst[n] = item
        value_lst[n] = dict[item]

    return render(request, "display_history.html", {"i0": input_lst[0], "i1":input_lst[1], "i2":input_lst[2], "i3":input_lst[3], "i4":input_lst[4], "i5":input_lst[5], "i6":input_lst[6], "i7":input_lst[7], "i8":input_lst[8], "i9":input_lst[9],
    "o0": value_lst[0], "o1": value_lst[1], "o2": value_lst[2], "o3": value_lst[3], "o4": value_lst[4], "o5":value_lst[5], "o6":value_lst[6], "o7":value_lst[7], "o8":value_lst[8], "o9":value_lst[9]
    })
