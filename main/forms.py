from django import forms
from .models import Post


class TopicForm(forms.Form):
    title = forms.CharField(label='Название темы', max_length=200)
    text = forms.CharField(label='Первое сообщение', widget=forms.Textarea(attrs={'rows': 5}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text': 'Твоё сообщение'}
        widgets = {'text': forms.Textarea(attrs={'rows': 4})}