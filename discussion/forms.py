from django import forms
from pagedown.widgets import PagedownWidget
from .models import Question, Answer

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    confirm_pass = forms.CharField(max_length=200)

class UpdateForm(forms.Form):
    name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    bio = forms.CharField(max_length=200)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    remember_me = forms.CharField(max_length=100)

class ChangePass(forms.Form):
    current = forms.CharField(max_length=100)
    new = forms.CharField(max_length=100)
    confirm_new = forms.CharField(max_length=100)

class AskQues(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = Question
        fields = {
            "title",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title of your question'}),
        }

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=1000)

class AnswerForm(forms.ModelForm):
    answer_text = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = Answer
        fields = {
            "answer_text",
        }
