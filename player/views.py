from django.shortcuts import render


# Create your views here.
def playerpage(request):
    context = {
        'src': '7WLIN_x67qQ',
    }
    return render(request, './player/playerpage.html', context)
