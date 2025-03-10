from pprint import pprint
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from cinema.cinema_logger import logger


def signup(request):
    """Page for user to create login"""
    if request.method == 'POST':

        # check if passwords are the same
        if request.POST['password'] != request.POST['password-confirmation']:
            return render(request, 'accounts/signup.html', {'error': 'Your passwords must match'})

        # check if it's a valid password. Password validation functions in the settings.py file.
        try:
            validate_password(request.POST['password'])
        except ValidationError:
            print(pprint(ValidationError))
            return render(request, 'accounts/signup.html', {'error': 'Invalid Password. Must be at least 8 characters'
                                                                     ' long and not similar to username.'})

        # check if username already exists
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'accounts/signup.html', {'error': 'Username already exists'})

        # create user if it doesn't work
        except User.DoesNotExist:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                logger.info("trying to sign up")
                auth.login(request, user)
                return redirect('screening_choice')
            # if user enters empty string
            except ValueError:
                return render(request, 'accounts/signup.html',
                              {'error': 'You must enter a reasonable username. No empty strings.'})

    # user wants to come to signup page
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    """Login page."""

    # if POST request, try to log in the user
    if request.method == 'POST':

        # authenticate user
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        # if authentication successful, login
        if user is not None:
            auth.login(request, user)
            return redirect('screening_choice')

        # return error if unsuccessful
        return render(request, 'accounts/login.html', {'error': 'username or password is wrong'})

    return render(request, 'accounts/login.html')


def logout(request):
    """Log out current user."""

    # log out
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')

    # get request redirects to different page
    return redirect('screening_choice')


class UpdateProfile(SuccessMessageMixin, UpdateView):
    """Page for updating email and name. Created using django generic class based views."""

    # parameters to be passed to special django view
    model = User
    fields = ['email', 'first_name', 'last_name']
    template_name = 'accounts/user_form.html'
    pk_url_kwarg = 'user_id'
    success_message = 'Details updated!'

    # specify user
    def get_object(self, queryset=None):
        return self.request.user

    # show this page on success
    def get_success_url(self):
        return reverse_lazy('update_profile')
