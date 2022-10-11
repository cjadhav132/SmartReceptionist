from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile,Meeting


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username','email','password1','password2')
        model = get_user_model()


class ProfileCreateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('birth_date',)


class ReceptionistLogin(forms.Form):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)


    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']


class CreateMeeting(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(CreateMeeting,self).__init__(*args,**kwargs)
        self.fields['employee'].disabled = True


    class Meta:
        model = Meeting
        fields = ('employee','visitor','purpose','start','end')




