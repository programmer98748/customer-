from django import forms
from .models import Comment

 

class CommentForm(forms.ModelForm):
    user_comment = forms.CharField(
        label="العنوان",
        widget=forms.TextInput(
            attrs={
            }
        )
    )
    email = forms.EmailField(
        required=True,
        label="البريد",

        widget=forms.EmailInput()
    )
    content  = forms.CharField(
        label="الرسالة",
        widget=forms.Textarea(),
        required=True
    )

    class Meta:
        model = Comment
        fields = ['email' ,'user_comment','content']


