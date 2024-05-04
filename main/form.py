from django.forms import ModelForm
from .models import Group

class Custom_form (ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        # exclude = None
