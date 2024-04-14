from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
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
    
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label=_('username'), help_text='', max_length=70)
    email = forms.EmailField(label=_('Email'), required=True)
    
    class Meta:
        model = User
        
        fields = ('first_name', 'last_name', 'username', 'email', 'groups', 'is_staff', 'is_active')
    def check_email(self, e_mail):
        email = self.cleaned_data.get('email')
        if email == e_mail:
            return self.cleaned_data
        if User.objects.filter(email=email).exists():
            self.clean_email(is_clean=False)
        return email      
    
    def clean_email(self, is_clean=True):
        if is_clean:
            return self.cleaned_data.get('email')
        else:
            raise forms.ValidationError('Email already exists.')
 

##
class LoginForm(forms.Form):
    username = forms.CharField(
         widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
##
class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
##


class PhotosForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
       

##
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']
##
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        labels = {
            'image' : 'رفع الصورة الشخصية'
        }
##
class InformaionSiteForm(forms.ModelForm):
    class Meta:
        model = InformaionSite
        fields = '__all__'
        

        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': ' الاسم',
            'image' : ' الصورة المعروضة',
            'description':' الوصف',
            'slug':'العنوان-كارابط-وصف',
        }
class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
        



class PagesForm(forms.ModelForm):
    class Meta:
        model = Pages
        fields = '__all__'
        labels = {
            'title': 'عنوان المقال',
            'image' : ' الصورة المعروضة',
            'description':' نص المقال'
        }
        exclude = ('',)


class PageAboutForm(forms.ModelForm):
    class Meta:
        model =PageAbout
        fields = '__all__'
        labels = {
            'description':'  الوصف',
            'title_head': 'مهمتنا',
            'title_goal' : 'رؤيتنا',
        }







from post.models import Post, PostLanguage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'language', 'active', 'published_at',)       
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs = {
            'placeholder':_('Write your title here')
        }
        
        self.fields['content'].widget.attrs = {
            'placeholder':_('Write content here')
        }

class PostLanguageForm(forms.ModelForm):
    class Meta:
        model = PostLanguage
        fields = ('post', 'language','title', 'content', 'active')       
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs = {
            'placeholder':_('Write your title here')
        }
        
        self.fields['content'].widget.attrs = {
            'placeholder':_('Write content here')
        }         

 




class BrandsForm(forms.ModelForm):
    class Meta:
        model = Brands
        fields = '__all__'
       
           