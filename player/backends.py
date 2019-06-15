from django.conf import settings
from player.models import Dj

class UsernameAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            dj = Dj.objects.get(username=username)
            if dj:
                return Dj
        except Dj.DoesNotExist:
            return None
