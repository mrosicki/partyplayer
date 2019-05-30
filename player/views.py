from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.forms import AuthenticationForm
from .forms import NameForm
from .models import dj

# Create your views here.


def playerpage(request):
    usernames = [i.username for i in dj.objects.all()]
    print(usernames)
    print(request.user.username)
    if request.user.username not in usernames:
        print(request.user.username)
        print("nie ma usera")
        return redirect('/player/login')
    context = {
        'src': '7WLIN_x67qQ',
    }
    return render(request, './player/playerpage.html', context)


def login(request):
    logout(request)
    if request.method == "POST":
        username=request.POST['username']
        form = NameForm(request.POST)
        request.user.username = username
        user = dj.create(username)
        user.save()
        print("lecimy tu " + username)
        return redirect('/player/playerpage')
    else:
        form = NameForm()
        print("no post")
    return render(request, './player/login.html', {'form': form})