from django.forms import ModelForm
from .models import Group, User

class Custom_form (ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['host', 'participants']


class Update_user_form (ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']