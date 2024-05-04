from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Group
from .form import Custom_form

def home (request):
    groups = Group.objects.all()
    return render(request, 'main/home.html', {'groups':groups})

def group (request, pk):
    group = Group.objects.get(id=pk)
    return render(request, 'main/group.html', {'group': group})

def create_group (request):
    form = Custom_form()
    if request.method == 'POST':
        form = Custom_form(request.POST)
        if(form.is_valid): 
            form.save()
            return redirect('main-home')
    return render(request, 'main/create_form.html', {'form': form})

def edit_group(request, pk):
    group = Group.objects.get(id=pk)
    form = Custom_form(instance=group)
    if request.method == 'POST':
        form = Custom_form(request.POST, instance=group)
        if(form.is_valid): 
            form.save()
            return redirect('main-home')
    return render(request, 'main/edit_group.html', {'form': form})