from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def homepage_view(request, *args, **kwargs):
    return render(request, 'pages/home.html')

def contact_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is a context test",
        "my_number": "This is a context number test"
    }
    return render(request, 'contact.html', my_context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('instructor/{}'.format(username))
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})

