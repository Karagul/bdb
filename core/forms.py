from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'name' : _('Имя'),
            'email': _('Почта'),
            'body' : _('Текст комментария'),
        }

class SearchForm(forms.Form):
    ORDER_CHOICES = (
        ('Moody', 'Рейтинг Moody'),
        ('Sp', 'Рейтинг S&P'),
        ('Fitch', 'Рейтинг Fitch'),
        ('Coupon', 'Купон'),
        ('Ticker', 'Тикер'),
        ('IssuerCompany', 'Имя эмитента'),
        ('Currency', 'Валюта'),
        ('Country', 'Страна эмитента'),
        ('Maturity', 'Дата погашения'),
    )
    
    search_string = forms.CharField(max_length=25, required=False, label='Имя эмитента')
    
    ordered_by = forms.ChoiceField(choices=ORDER_CHOICES, required=False, label='Сортировать по')
    descending = forms.BooleanField(initial=True, required=False, label='По убыванию')

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class UploadForm(forms.Form):
    file_ = forms.FileField(label='Имя файла')
