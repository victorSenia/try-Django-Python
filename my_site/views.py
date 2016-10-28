from django.contrib.auth.hashers import make_password
from django.forms.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from my_site.forms import UserForm, propertyFormSet, meetingFormSet, clientForm
from my_site.models import Client, User


def index(request):
    return render(request, 'my_site/index.html', {'users': User.objects.all(), 'clients': Client.objects.all(), })


def user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            # data = serializers.serialize('json', [user])
            # return JsonResponse(data)
            return HttpResponseRedirect(reverse(userInfo, args=(user.id,)))
    else:
        form = UserForm
    return render(request, 'my_site/create.html', {'form': form, "title": "user"})


def client(request):
    if request.method == "POST":
        form = clientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=True)
            return HttpResponseRedirect(reverse(clientInfo, args=(client.id,)))
    else:
        form = clientForm
    return render(request, 'my_site/create.html', {'form': form, "title": "client"})


def userInfo(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = propertyFormSet(request.POST, instance=user)
        if form.is_valid():
            properties = form.save(commit=True)
            return HttpResponseRedirect(reverse(userInfo, args=(id,)))
    else:
        form = propertyFormSet(instance=user)
    return render(request, 'my_site/user.html', {'user': user, 'form': form})


def clientInfo(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == "POST":
        form = meetingFormSet(request.POST, instance=client)
        if form.is_valid():
            meetings = form.save(commit=True)
            return HttpResponseRedirect(reverse(clientInfo, args=(id,)))
    else:
        form = meetingFormSet(instance=client)
    return render(request, 'my_site/client.html', {'client': client, 'form': form})


def userDelete(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            user.delete()
    return HttpResponseRedirect(reverse(index))


def clientDelete(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            client.delete()
    return HttpResponseRedirect(reverse(index))
