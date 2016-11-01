from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.forms import Form
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from my_site.forms import UserForm, propertyFormSet, meetingFormSet, OwnerForm, clientForm
from my_site.models import Client, Owner


def index(request):
    # users = getDictionary(Owner.objects.all(), exclude=["password", "last_login", "is_active", "is_admin"], deepth=5)
    # clients = getDictionary(Client.objects.all(), exclude=["password", "last_login", "is_active", "is_admin"], deepth=5)
    # return JsonResponse({"users": users, "clients": clients})
    # clients = getDictionary(UserProfile.objects.all())
    # meeting = getDictionary(UserProfile.objects.all(), deepth=5)
    # meeting = getDictionary(Meeting.objects.all(), deepth=5)
    # return JsonResponse({"meeting": meeting})
    return render(request, 'my_site/views/index.html',
                  {'users': Owner.objects.all(), 'clients': Client.objects.all(), })


def user(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        form = OwnerForm(request.POST)
        if user_form.is_valid() & form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            owner = form.save(commit=False)
            owner.user = user
            owner.save()
            return redirect('my_site:userInfo', id=owner.id)
    else:
        user_form = UserForm()
        form = OwnerForm()
    return render(request, 'my_site/views/create.html', {'form': [form, user_form], "title": "user"})


def client(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        form = clientForm(request.POST)
        if user_form.is_valid() & form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            client = form.save(commit=False)
            client.user = user
            client.save()
            return redirect('my_site:clientInfo', id=client.id)
    else:
        user_form = UserForm()
        form = clientForm()
    return render(request, 'my_site/views/create.html', {'form': [form, user_form], "title": "client"})


@login_required
def userInfo(request, id):
    user = get_object_or_404(Owner, pk=id)
    if request.method == "POST":
        form = propertyFormSet(request.POST, instance=user)
        if form.is_valid():
            properties = form.save(commit=True)
            return redirect('my_site:userInfo', id=id)
    else:
        form = propertyFormSet(instance=user)
    return render(request, 'my_site/views/user.html', {'owner': user, 'form': form})


def checkUser(user):
    # userProfile=UserProfile.objects.get(user=user)
    return user.username != "aasd"


# @login_required
@user_passes_test(checkUser)
def clientInfo(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == "POST":
        form = meetingFormSet(request.POST, instance=client)
        if form.is_valid():
            meetings = form.save(commit=True)
            return redirect('my_site:clientInfo', id=id)
    else:
        form = meetingFormSet(instance=client)
    return render(request, 'my_site/views/client.html', {'client': client, 'form': form})


@login_required
def userDelete(request, id):
    user = get_object_or_404(Owner, pk=id)
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            user.user.delete()
    return redirect('my_site:index')


@login_required
def clientDelete(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            client.user.delete()
    return redirect('my_site:index')


# def register(request):
#     # A boolean value for telling the template whether the registration was successful.
#     # Set to False initially. Code changes value to True when registration succeeds.
#     registered = False
#
#     # If it's a HTTP POST, we're interested in processing form data.
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save(commit=False)
#
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
#
#             # Now sort out the UserProfile instance.
#             # Since we need to set the user attribute ourselves, we set commit=False.
#             # This delays saving the model until we're ready to avoid integrity problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             # Did the user provide a profile picture?
#             # If so, we need to get it from the input form and put it in the UserProfile model.
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             # Now we save the UserProfile model instance.
#             profile.save()
#
#             # Update our variable to tell the template registration was successful.
#             registered = True
#
#         # Invalid form or forms - mistakes or something else?
#         # Print problems to the terminal.
#         # They'll also be shown to the user.
#         else:
#             print(user_form.errors, profile_form.errors)
#
#     # Not a HTTP POST, so we render our form using two ModelForm instances.
#     # These forms will be blank, ready for user input.
#     else:
#         user_form = UForm()
#         profile_form = UserProfileForm()
#
#     # Render the template depending on the context.
#     return render(request, 'my_site/views/register.html',
#                   {'form': [user_form, profile_form], 'registered': registered}, )


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('my_site:index')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'my_site/views/login.html', )


@login_required
def user_logout(request):
    logout(request)
    return redirect('my_site:index')
