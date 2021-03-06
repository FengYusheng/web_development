from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form':ItemForm()})


def new_list(request):
    list_ = List.objects.create()
    form = ItemForm(data=request.POST)
    if form.is_valid():
        form.save(for_list=list_)
        return redirect(list_)
    list_.delete()
    return render(request, 'home.html', {'form':form})
