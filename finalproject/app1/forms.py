from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from app1.models import CustomUser, Post


class CreateUserForm(UserCreationForm):
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    )

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password1','password2','gender']



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','post_img']
        
    post_img = forms.ImageField(required=False)