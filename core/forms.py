from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form):
    ORDER_CHOICES = (
        ('Coupon', 'Купон'),
        ('Moody', 'Рейтинг Moody'),
        ('Ticker', 'Тикер'),
        ('IssuerCompany', 'Имя эмитента'),
        ('Currency', 'Валюта'),
    ) # Добавить все варианты
    
    search_string = forms.CharField(max_length=25, required=True, label='Слово')
    # Добавить поля поиска
    ordered_by = forms.ChoiceField(choices=ORDER_CHOICES, required=False, label='Сортировать по')
    descending = forms.BooleanField(initial=True, required=True, label='По убыванию')

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class UploadForm(forms.Form):
    file_ = forms.FileField(label='Имя файла')
