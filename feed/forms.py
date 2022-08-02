from django import forms
from django.contrib.auth.models import User
from common.models import User
from author.models import Author
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from froala_editor.widgets import FroalaEditor


class AuthorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = Author
        fields = ('password', 'confirm_password',
                  'email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super(AuthorForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "passwords do not match"
            )
    helper = FormHelper()


class AuthorEditForm(forms.ModelForm):

    class Meta():
        model = Author
        fields = (
            'email', 'first_name', 'last_name')

    helper = FormHelper()


class AuthorProfileForm(forms.ModelForm):
    class Meta():
        model = Author
        fields = ('bio', 'avatar')
    helper = FormHelper()


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'tags', 'content', 'image')

        widgets = {
            'title': forms.Textarea(attrs={'class': 'post-title-input', 'placeholder': 'Title'}),
            'content': FroalaEditor(),
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('content',)

    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Write a response"
