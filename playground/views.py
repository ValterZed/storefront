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


def generate(text, settings):

    prompt = (GoogleTranslator('auto','en').translate(text))

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"write '{prompt}' in a new way" if rewrite else prompt,
        temperature=float(settings["temperature"]),
        max_tokens=int(settings["max_tokens"]),
        top_p=1,
        frequency_penalty=float(settings["frequency_penalty"]),
        presence_penalty=float(settings["presence_penalty"])
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

        try:
            with open(f"playground\data\{ip}\history.json", "w+") as json_file:
                dump_dict = {}
        except:
            os.mkdir(f"playground\data\{ip}")
        with open(f"playground\data\{ip}\history.json", "w+") as json_file:
            dump_dict = {}
            json.dumps(dump_dict)
        with open(f"playground\data\{ip}\settings.json", "w+") as json_file:
            dump_dict = {"temperature": 0.7, "max_tokens": 256, "frequency_penalty": 2, "presence_penalty": 0}
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
        with open(f"playground\data\{ip}\settings.json", "r+") as json_file:
            try: 
                user_settings = json.loads(json_file.read())
            except:
                user_settings = ai_values
                with open(f"playground\data\{ip}\settings.json", "w+") as json_a_file:
                    json_a_file.write(json.dumps(user_settings))
        query = q
        gen_text = generate(query, user_settings)

        try:
            with open(f"playground\data\{ip}\history.json", "r+") as json_file:
                dict = json.loads(json_file.read())
        except:
            with open(f"playground\data\{ip}\history.json", "w+") as json_file:
                json_file.write(json.dumps({}))
                dict = {}
        with open(f"playground\data\{ip}\history.json", "w+") as json_file:
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
    input_lst = []
    value_lst = []
    with open(f"playground\data\{ip}\history.json", "r+") as json_file:
        dict = json.loads(json_file.read())
    
    for n, item in enumerate(reversed(dict.keys())):
        input_lst.append(item.replace(",","£$"))
        value_lst.append(dict[item].replace(",","£$"))

    return render(request, "display_history.html", {"input_list": input_lst, "output_list": value_lst})

def settings(request):
    ip = get_client_ip(request)
    with open(f"playground\data\{ip}\settings.json", "r+") as json_file:
        user_settings = json.loads(json_file.read())

    if request.GET.get('t') != None:
        user_settings["temperature"] = request.GET.get('t')
        user_settings["max_tokens"] = request.GET.get('mt')
        user_settings["frequency_penalty"] = request.GET.get('fp')
        user_settings["presence_penalty"] = request.GET.get('pp')

        with open(f"playground\data\{ip}\settings.json", "w+") as json_file:
            json_file.write(json.dumps(user_settings))
        
        return render(request, "redirect_home.html",)

    return render(request, "settings.html", {"temperature": user_settings["temperature"], "max_tokens": user_settings["max_tokens"], "frequency_penalty": user_settings["frequency_penalty"], "presence_penalty": user_settings["presence_penalty"], "ip":ip})
