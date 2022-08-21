from django import forms
from .models import User, PostResult
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        error_messages={'required': '아이디을 입력해주세요.'},
        max_length=17,
        label='아이디'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
        error_messages={'required': '비밀번호를 입력해주세요.'},
        label='비밀번호'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
               user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return
            
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')

class PostForm(forms.ModelForm):
    team_name = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        error_messages={'required': '팀명을 입력해주세요.'},
        max_length=17,
        label='팀명'
    )
    team_members = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        error_messages={'required': '팀원을 입력해주세요.'},
        max_length=40,
        label='팀원'
    )
    intro_text = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        error_messages={'required': '한줄소개를 입력해주세요.'},
        max_length=100,
        label='한줄소개'
    )
    class Meta:
        model = PostResult
        fields = ['team_name', 'team_members', 'intro_text', 'image1', 'image2','image3','image4']
