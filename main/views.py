from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Group, Topic
from .form import Custom_form
from django.db.models import Q

def home (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    groups = Group.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(discription__icontains=q)
    )
    topics = Topic.objects.all()
    return render(request, 'main/home.html', {'groups':groups, 'topics': topics})

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

def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('main-home')
    return render(request, 'main/delete_group.html', {'obj': group.name})