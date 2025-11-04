from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Message
from django.db.models import Q
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back, " + username + " 👋")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'home/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')



@login_required
def index(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted successfully! ✅")
            return redirect('index')
        else:
            messages.error(request, "Something went wrong. Please check your form.")
    else:
        form = MessageForm()
    return render(request, 'home/index.html', {'form': form})


@login_required
def message_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        messages = Message.objects.filter(
            Q(username__icontains=search_query) | Q(message__icontains=search_query)
        )
    else:
        messages = Message.objects.all()

    paginator = Paginator(messages, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }
    return render(request, 'home/message_list.html', context)




def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password == confirm:
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.warning(request, "Email already registered.")
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Account created successfully! Please log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'home/register.html')

