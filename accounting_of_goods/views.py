from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from .models import Main_table, Operation, Category
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Case, IntegerField, Sum, Value, When
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models import Q
from .forms import *
import datetime

def getCountFromBase(inputProduct, inputDivision):
    result = (
        Main_table.objects
            .filter(product=inputProduct, division=inputDivision)
            .aggregate(
            total_quantity=Coalesce(
                Sum(
                    Case(
                        When(operation__id_operation='1', then=-1),  # определение приход товара или расход
                        default=1,
                        output_field=IntegerField()
                    ) * F('count')
                ),
                0
            )
        )
    )
    total_quantity = result['total_quantity']

    return total_quantity

def search(request, result, useDate = True):
    combinedFilterForm = CombinedFilterForm(request.GET)
    if combinedFilterForm.is_valid():
        categories = combinedFilterForm.cleaned_data['categories']
        divisions = combinedFilterForm.cleaned_data['divisions']
        search_query = combinedFilterForm.cleaned_data['search']
        dateRange = combinedFilterForm.cleaned_data['dateRange']

        if dateRange and useDate:
            date_time_objs = dateRange.split(' - ')
            date_time_objs = map(lambda x: datetime.datetime.strptime(x,'%d/%m/%Y'), date_time_objs)
            date_time_objs = map(lambda x : x.strftime('%Y-%m-%d') ,date_time_objs)
            result = result.filter(date__range = date_time_objs)

        if categories:
            result = result.filter(category__id_category__in=categories)  # фильтр по категориям
        if divisions:
            result = result.filter(division__id_division__in=divisions)  # фильтр по категориям

        if search_query:
            result = result.filter(
                Q(category__name__icontains=search_query) |
                Q(product__name_lower__icontains=search_query) |
                Q(product__name__icontains=search_query)
            )  # поиск по категории и названию
        return result, combinedFilterForm

def index(request): # отображение главной страницы
    result = (
        Main_table.objects
            .values('product__name', 'category__name', 'category','product','division__id_division','division__name')
            .annotate(
            sum_price=Coalesce(
                Sum(    # подсчет суммы количества товаров
                    Case(
                        When(operation__id_operation='1', then=-1), # определение приход товара или расход
                        default=1,
                        output_field=IntegerField()
                    ) * F('count')
                ),
                0
            )
        )
            .order_by('division__name','category__name') # группировка по категории
    )   # большой запрос для отображения информации о товарах на странице

    result, combinedFilterForm = search(request, result, False)
    combinedFilterForm.fields['dateRange'].disabled = True

    addForm = Main_tableForm()
    error=''
    if request.method == "POST":
        main_tableForm =  Main_tableForm(request.POST)
        if main_tableForm.is_valid():
            count = getCountFromBase(main_tableForm.cleaned_data['product'], main_tableForm.cleaned_data['division'])
            if main_tableForm.cleaned_data['operation'].id_operation == 1 and main_tableForm.cleaned_data['count'] > count:
                return JsonResponse({"error": "Invalid data provided.", "count": count}, status=400)
            else:
                main_tableForm.save()
                request.META.get('HTTP_REFERER')
            return redirect('/')
        else:
            error = 'Форма заполнена неверно'
    context = {
        'rows': result,
        'combinedFilterForm' : combinedFilterForm,
        'addForm': addForm,
        'error': error,
    }
    return render(request, 'accounting_of_goods/homePage.html', context)

def contact(request):   # страница информации
    phones = '8(914) 487-31-10','X(XXX) XXX-XX-XX'
    return  render(request,'accounting_of_goods/contact.html',{'values' : phones})
def adm(request):   # заглушка для отображения страницы admin
    pass
def consumption(request):
    return receiptOrConsumption(request, type = 1)  # отображение страницы расхода товара
def receipt(request):
    return receiptOrConsumption(request, type = 0)  # отображение страницы поступления товара
    # type = 0
def receiptOrConsumption(request, type):
    result = Main_table.objects.filter(operation=type).order_by('-date')  # фильтр по типу операции

    result, combinedFilterForm = search(request,result) # все остальные фильтры

    entries_per_page = 5   # количество записей на странице
    # pageSize = PageSize(request.GET)    # форма количества записей на странице
    # if pageSize.is_valid():
    #     page = pageSize.cleaned_data['count']
    #     if page:
    #         entries_per_page = page

    page_number = request.GET.get('page', 1)
    paginator = Paginator(result, entries_per_page)
    try:
        result = paginator.page(page_number)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    addForm = Main_tableForm( initial = {
        'operation' : type,
    })
    error = ''
    if request.method == "POST":
        main_tableForm = Main_tableForm(request.POST)
        # print(main_tableForm.errors.as_data())
        if main_tableForm.is_valid():
            count = getCountFromBase(main_tableForm.cleaned_data['product'], main_tableForm.cleaned_data['division'])
            if main_tableForm.cleaned_data['operation'].id_operation == 1 and main_tableForm.cleaned_data['count'] > count:
                return JsonResponse({"error": "Invalid data provided.","count" : count}, status=400)
            else:
                main_tableForm.save()
                request.META.get('HTTP_REFERER')
            #return  redirect('/')
        else:
            error = 'Форма заполнена неверно'
    context = {
        'rows': result,
        'type': type,
        'combinedFilterForm': combinedFilterForm,
        'addForm' : addForm,
        # 'pageSize' : pageSize,
        'error' : error,
    }
    return render(request, 'accounting_of_goods/receiptAndConsumptionPage.html', context)