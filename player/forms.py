from django import forms


class NameForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)

    def get_username(self):
        return self.username

class LinkForm(forms.Form):
    link = forms.CharField(label='link', max_length=1000)

    def get_link(self):
        return self.link