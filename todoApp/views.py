from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'todoApp/home.html')


def signupuser(request):
    form = UserCreationForm()
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        print(username, password1)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todoApp/signupuser.html', {'form': form, 'error': f"'{username}' is already taken. Please choose a new username."})
        else:
            return render(request, 'todoApp/signupuser.html', {'form': form, 'error': "Passwords did not matched!"})
    return render(request, 'todoApp/signupuser.html', {'form': form})


def loginuser(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'todoApp/loginuser.html', {"form": form, "error": "Username and password did not match."})
    return render(request, "todoApp/loginuser.html", {"form": form})


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return redirect('home')


def currenttodos(request):
    return render(request, "todoApp/currenttodos.html")
