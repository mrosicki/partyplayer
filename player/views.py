from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import NameForm, LinkForm
from .models import Song
import json
from urllib.parse import urlparse, parse_qs


# Create your views here.

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


def get_next():
    try:
        return Song.objects.filter(wasPlayed=False).order_by('pk')[:1][0]
    except IndexError:
        return None

def add_song(request):
    link = request.POST.get('link')
    if link:
        song = Song(dj=request.user, link=link)
        song.save()
        return HttpResponse(status=200)
    return HttpResponse(status=500)

def playerpage(request):

    #dodawanie piosenki do playlisty
    if request.method == "POST":
        link = request.POST['link']
        song = Song()
        song.dj = request.user
        song.link = link
        song.save()
        return redirect('/player/playerpage')

    #sprawdzenie czy uzytkownik ustawil sobie nick
    usernames = [i.username for i in User.objects.all()]
    print(usernames)
    print(request.user.username)
    if request.user.username not in usernames:
        print(request.user.username)
        print("nie ma usera")
        return redirect('/player/login')
    form = LinkForm()
    songToPlay = get_next()
    print(get_next())
    if songToPlay:
        src = video_id(songToPlay.link)
        songToPlay.wasPlayed = True
        songToPlay.save()
    else:
        src = ''
    
    print(src)
    playlist = [i for i in Song.objects.all()]
    context = {
        'src': src,
        'form': form,
        'playlist': playlist
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
        # print("no post")
    return render(request, './player/login.html', {'form': form})
