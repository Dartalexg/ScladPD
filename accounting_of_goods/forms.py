from django import forms
from django.forms import ModelForm
from .models import *

class CategoryFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class ProductFilterForm(forms.Form):    # форма поиска
    search = forms.CharField(label="Search", max_length=100, required=False)
    search.widget.attrs.update({'class': 'form-control', ' placeholder': 'Поиск'})

class CombinedFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    divisions = forms.ModelMultipleChoiceField(
        queryset=Division.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    dateRange = forms.CharField(label='диапазон дат', max_length=100, required=False,
                                widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Диапазон дат', 'id' : 'dateRangePicker','autocomplete':'off'}))

    search = forms.CharField(label="Search", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск', 'id' : 'searchInput'}))
    # def __init__(self, *args, **kwargs):
    #     showDateInput = kwargs.pop('showDateInput')
    #     if showDateInput == False:
    #         self.dateRange.widget_attrs({'disabled' : True})
    #     super(CombinedFilterForm, self).__init__(*args, **kwargs)

class Main_tableForm(ModelForm):
    # hidden_category = forms.CharField(widget=forms.HiddenInput())
    # product_hidden_field = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Main_table
        fields = ['category', 'product', 'count', 'operation', 'date', 'division']
        labels = {
            'category': 'Категория',
            'product': 'Продукт',
            'count': 'Количество',
            'operation': 'Тип операции',
            'date': 'Дата',
            'division': 'Отдел',
        }
        widgets = {
            'category': forms.Select(attrs={'id': 'categoryInput','disabled':False}),
            'product': forms.Select(attrs={'id': 'productInput','disabled':False}),
            'count': forms.NumberInput(attrs={'min': 0, 'max': 10000, 'id' : 'countInput'}),
            'operation' : forms.Select(attrs={'id': 'operationInput'}),
            'date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}
            ),
            'division': forms.Select(attrs={'id': 'divisionInput'}),
        }

    def __init__(self ,*args, **kwargs):
        super(Main_tableForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PageSize(forms.Form):    # форма поиска
    count = forms.IntegerField(min_value=1, max_value=1000, required=False)
    count.label = "Записей на странице"
    count.widget.attrs.update({'class': 'form-control'})