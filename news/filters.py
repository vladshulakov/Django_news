from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter, DateFromToRangeFilter
from django import forms

from news.models import Author


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(FilterSet):
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

    title = CharFilter(
        field_name='title',
        lookup_expr='contains',
        label='Title'
    )