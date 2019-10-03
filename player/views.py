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
        if 'youtube' in link or 'youtu.be' in link:
            website = 'youtube'
        else:
            website = 'soundcloud'    
        song = Song(dj=request.user, link=link, website=website)
        song.save()
        return HttpResponse(status=200)
    return HttpResponse(status=500)

def playerpage(request):

    #check whether user has set an username
    usernames = [i.username for i in User.objects.all()]
    if request.user.username not in usernames:
        return redirect('/player/login')
    form = LinkForm()
    songToPlay = get_next()
    if songToPlay:
        if songToPlay.website == 'youtube':
            src = video_id(songToPlay.link)
        else:
            src = songToPlay.link
        songToPlay.wasPlayed = True
        website = songToPlay.website
        songToPlay.save()
    else:
        src = ''
        website = ''
    
    playlist = [i for i in Song.objects.all()]
    
    context = {
        'src': src,
        'form': form,
        'playlist': playlist,
        'website': website
    }
    return render(request, './player/playerpage.html', context)


def test_soundcloud(request):
    return render(request, './player/test_soundcloud.html')


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
    return render(request, './player/login.html', {'form': form})
