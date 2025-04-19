from django import forms
from .models import Task, Coment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        exclude = ['user'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ('content', "coment_pic")
