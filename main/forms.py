from django import forms
from .models import Post, Profile


class TopicForm(forms.Form):
    title = forms.CharField(label='Название темы', max_length=200)
    text = forms.CharField(label='Первое сообщение', widget=forms.Textarea(attrs={'rows': 4}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text': 'Сообщение'}
        widgets = {'text': forms.Textarea(attrs={'rows': 3})}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Я люблю...'}),
        }