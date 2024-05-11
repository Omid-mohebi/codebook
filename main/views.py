from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Group, Topic, Message
from .form import Custom_form
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    groups = Group.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(discription__icontains=q) |
        Q(host__username__icontains=q)
    )


    topics = Topic.objects.all()
    return render(request, 'main/home.html', {'groups':groups, 'topics': topics, 'group_count': groups.count()})

def login_veiw(request):

    if request.user.is_authenticated: redirect('main-home')

    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == 'POST':
        try:
            temp = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main-home')
            else:
                messages.error(request, 'Password is incorrect!')
        except:
            messages.error(request, 'This username does not exist!')
    return render(request, 'main/login.html')

@login_required(login_url='login')
def logout_veiw(request):
    logout(request)
    return redirect('main-home')

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('main-home')
        else:
            messages.error(request, 'Sign up faild..')
    return render(request, 'main/register.html', {'form': form})

def group (request, pk):
    group = Group.objects.get(id=pk)
    messages = group.message_set.all().order_by('-created')
    participants = group.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            sender = request.user,
            group = group,
            body = request.POST.get('comment'),
        )
        return redirect('group-veiw', pk=group.id)
    return render(request, 'main/group.html', {'group': group, 'messages': messages, 'participants': participants})

@login_required(login_url='login')
def create_group (request):
    form = Custom_form()
    if request.method == 'POST':
        form = Custom_form(request.POST)
        if(form.is_valid): 
            form.save()
            return redirect('main-home')
    return render(request, 'main/create_form.html', {'form': form})

@login_required(login_url='login')
def edit_group(request, pk):
    group = Group.objects.get(id=pk)
    form = Custom_form(instance=group)
    if request.user != group.host: return HttpResponse('<h1>You are not alowed here!</h1>')
    if request.method == 'POST':
        form = Custom_form(request.POST, instance=group)
        if(form.is_valid): 
            form.save()
            return redirect('main-home')
    return render(request, 'main/edit_group.html', {'form': form})

@login_required(login_url='login')
def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.user != group.host: return HttpResponse('<h1>You are not alowed here!</h1>')
    if request.method == 'POST':
        group.delete()
        return redirect('main-home')
    return render(request, 'main/delete_group.html', {'obj': group.name})