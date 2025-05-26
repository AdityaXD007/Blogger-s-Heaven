from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 'category', 'excerpt', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-input', 'placeholder': 'Enter a descriptive title', 'id': 'post-title'}),
            'featured_image': forms.FileInput(attrs={'class': 'file-input', 'id': 'post-featured-image'}),
            'category': forms.Select(attrs={'id': 'post-category'}),
            'excerpt': forms.Textarea(attrs={'class': 'excerpt-input', 'rows': 3, 'placeholder': 'Write a brief summary of your post', 'id': 'post-excerpt'}),
            'content': forms.Textarea(attrs={'class': 'content-input', 'rows': 15, 'placeholder': 'Start writing your post here...', 'id': 'post-content'}),
            'tags': forms.TextInput(attrs={'class': 'tags-input', 'placeholder': 'Add tags separated by commas', 'id': 'post-tags'}),
        }
