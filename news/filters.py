from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from django import forms

from news.models import Author, Category


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='contains',
        label='Title'
    )
    
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='Не выбрано'
    )

    date_gt = DateFilter(
        field_name='time_create',
        lookup_expr='gt',
        label='Date',
        widget=DateInput
    )

    category = ModelChoiceFilter(
        field_name='categories',
        label='Category',
        empty_label='Все категории',
        queryset=Category.objects.all())

