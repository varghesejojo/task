from .models import BlogPost
from django import forms
from .models import Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields=["image","title","content","author"]




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),  # Customize the text area appearance
        }
        labels = {
            'text': 'Your Comment',  # Customize the label for the text field
        }