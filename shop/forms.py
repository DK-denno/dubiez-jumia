from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Messages,Address


class signUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='')
    last_name =  forms.CharField(max_length=30, required=True, help_text='')
    username =  forms.CharField(max_length=30, required=True, help_text='')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2', ]

class changePasswordForm(forms.Form):
    username = forms.CharField(max_length=30, help_text='',label='',  widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    
class profileForm(forms.ModelForm):
    firstname = forms.CharField(max_length=30,required=True,help_text="Enter Your firstname,whether current or new")
    lastname = forms.CharField(max_length=30,required=True,help_text='Enter Your lastname,whether current or new')
    username = forms.CharField(max_length=30, required=True, help_text='Enter Your username,whether current or new')
    email = forms.EmailField(max_length=30,required=True,help_text='Enter Your Email,whether current or new')
    class Meta:
        model = Profile
        fields = ['username','firstname','lastname','email','phone_number']

class chatForm(forms.ModelForm):
    message =  forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":45}))
    class Meta:
        model = Messages
        fields = ['message']

class addressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city','town']