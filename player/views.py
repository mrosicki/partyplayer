from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.forms import AuthenticationForm
from .forms import NameForm
from django.contrib.auth.models import User

# Create your views here.


def playerpage(request):
    usernames = [i.username for i in User.objects.all()]
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


def loginpage(request):
    logout(request)
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username)
        authenticate(user)
        login(request, user)
        return redirect('/player/playerpage')
    else:
        form = NameForm()
        print("no post")
    return render(request, './player/login.html', {'form': form})
