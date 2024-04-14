from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

        
class UserForm(forms.ModelForm):
    username = forms.CharField(label=_('username'), help_text='', max_length=70)
    password = forms.CharField(label=_('Password'), min_length=8, max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('Confirm Password'), min_length=8, max_length=50, widget=forms.PasswordInput())
    email = forms.EmailField(label=_('Email'), required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2','groups', 'is_staff', 'is_active')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('The two password fields didn’t match.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email  
   




class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': _('Email or Username')}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':_('Password')}))


'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        user = User.objects.get(username=username)
        
        if User.objects.filter(email=email).count() > 1:
            raise forms.ValidationError('Email already exists.')        
   
        return email      
    
                '''