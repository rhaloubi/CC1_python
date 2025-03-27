from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Category

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Add Bootstrap classes to the default form fields
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Customize help texts
        self.fields['username'].help_text = "Requis. 150 caractères ou moins. Uniquement des lettres, chiffres et @/./+/-/_."
        self.fields['password1'].help_text = "Votre mot de passe doit contenir au moins 8 caractères et ne peut pas être entièrement numérique."
        self.fields['password2'].help_text = "Entrez le même mot de passe que précédemment, pour vérification."

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'author_name']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom (pour les utilisateurs non inscrits)'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['author_name'].widget = forms.HiddenInput()
            self.fields['author_name'].required = False 