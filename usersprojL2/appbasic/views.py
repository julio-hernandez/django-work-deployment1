from django.shortcuts import render
from appbasic.forms import UserForm, UserProfileInfoForm

# imports for login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.


def indexView(request):
    return render(request, 'appbasic/index.html')


@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def specialView(request):
    return HttpResponse('You are in')


def registerView(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=True)
            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print("Picture detected")
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True

    else:
        user_form = UserForm()
        user_profile_form = UserProfileInfoForm()

    data_dict = {'registered': registered, 'user_form': user_form,
                 'user_profile_form': user_profile_form}
    return render(request, 'appbasic/register.html', context=data_dict)


# The login view
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user, backend=None)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('Someone tried to login and failed')
            print("Username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'appbasic/login.html')
