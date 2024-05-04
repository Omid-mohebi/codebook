from django.shortcuts import render
from django.http import HttpResponse

groups = [
    {'id':1, 'name': 'python'},
    {'id':2, 'name': 'c#'},
    {'id':3, 'name': 'C++'},
]

def home (request):
    return render(request, 'main/home.html', {'groups':groups})

def group (request, pk):
    return render(request, 'main/group.html', {'group': groups[int(pk)-1]})