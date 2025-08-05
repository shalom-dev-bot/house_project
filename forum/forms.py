from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-zinc-800 text-white'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-2 rounded bg-zinc-800 text-white'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full p-2 rounded bg-zinc-800 text-white'}),
        }
