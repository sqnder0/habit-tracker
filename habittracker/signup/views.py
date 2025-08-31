from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse

# Create your views here.
def signup(request: HttpRequest):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, "registration/signup.html", {"form": form})