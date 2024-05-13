from django.shortcuts import render, redirect
from .models import Group, Topic, Message
from .form import Custom_form
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

def home (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    groups = Group.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(discription__icontains=q) |
        Q(host__username__icontains=q)
    )

    msgs = []
    for group in groups:
        msgs+=group.message_set.all()
    topics = Topic.objects.all()
    return render(request, 'main/home.html', {
        'groups':groups, 
        'topics': topics, 
        'group_count': groups.count(),
        'msgs': msgs,
        })

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
    messages = group.message_set.all().order_by('created')
    participants = group.participants.all()
    print(messages)
    if request.method == 'POST':
        if request.user not in participants:
            group.participants.add(request.user)
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

def delete_message(request, pk1, pk2):
    group = Group.objects.get(id=pk1)
    if group.message_set.get(id=pk2):
        message = group.message_set.get(id=pk2)
    if request.user != message.sender: return HttpResponse('<h1>You are not alowed here!</h1>')
    if request.method == 'POST':
        message.delete()
        return redirect('main-home')
    return render(request, 'main/delete_message.html', {'obj': message.body})

def users_profile (request, pk):
    user = User.objects.get(id=pk)
    groups = user.group_set.all()
    topics = Topic.objects.all()
    msgs = user.message_set.all()

    return render(request, 'main/users_profile.html', {
        'groups':groups, 
        'topics': topics, 
        'group_count': groups.count(),
        'msgs': msgs,
    })