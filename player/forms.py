from django import forms


class NameForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)

    def get_username(self):
        return self.username

