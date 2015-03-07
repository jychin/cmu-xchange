from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from xchange.models import *
from xchange.forms import *
from django.http import HttpResponse, Http404
from django.core import serializers
import json

from django.views.decorators.csrf import csrf_exempt

@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    items = Item.objects.all().order_by('-time')
    
    #comments = Comment.objects.all().order_by('time')
    context = {'items': items}
    return render(request, 'xchange/globalstream.html', context)

@login_required
def followstream(request):
    templist = request.user.profile.follower.all().order_by('-time')
    items = Item.objects.filter(user__in=templist)
    context = {'items' : items}
    return render(request, 'xchange/followstream.html', context)


@login_required
def profile(request, id):
    tempuser = get_object_or_404(User, id=id)

    tempprofile = tempuser.profile
    items = Item.objects.filter(user=tempuser).order_by('-time')
    state = "1"
    if request.user.profile == tempprofile:
        state = "3"
    elif request.user.profile.follower.all().filter(profile_user__exact=tempuser):
        state = "2"
    return render(request, 'xchange/profile.html', {'user':tempuser, 'items' : items, 'profile':tempprofile, 'state':state})

@login_required
def follow(request, id):
    tempuser = User.objects.filter(id=id)[0]
    tempprofile = tempuser.profile
    request.user.profile.follower.add(tempprofile)
    return redirect(reverse('profile', args=(id,)))

@login_required
def unfollow(request, id):
    tempuser = User.objects.filter(id=id)[0]
    tempprofile = tempuser.profile
    request.user.profile.follower.remove(tempprofile)
    return redirect(reverse('profile', args=(id,)))

@login_required
def edit_profile(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = CreateForm()
        return render(request, 'xchange/edit_profile.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    new_profile =  request.user.profile
    print request.FILES
    form = CreateForm(request.POST, request.FILES, instance=new_profile)
    


    if not form.is_valid():
        context['form'] = form
        return render(request, 'xchange/edit_profile.html', context)
    else:
        if form.cleaned_data['photo']:
            new_profile.content_type = form.cleaned_data['photo'].content_type
            print 'content type =', form.cleaned_data['photo'].content_type
        form.save()
        context['message'] = 'Item #{0} saved.'.format(new_profile.id)
        #context['form'] = CreForm()
        return redirect(reverse('profile', args=(request.user.id,)))


@login_required
@transaction.atomic
def add_item(request):
    errors = []
    # Creates a new item if it is present as a parameter in the request
    if not 'item' in request.POST or not request.POST['item']:
    	errors.append('You must enter an item to add.')
    else:
        if len(request.POST['item']) > 160:
            errors.append('You must enter less than 160 characters.')
            items = Item.objects.all().order_by('-time')
            context = {'items' : items, 'errors' : errors}
            return render(request, 'xchange/globalstream.html', context)
    	new_item = Item(text=request.POST['item'], user=request.user.profile)
    	new_item.save()
    items = Item.objects.all().order_by('-time')
    context = {'items' : items, 'errors' : errors}
    return redirect(reverse('home'))
    #return render(request, 'xchange/globalstream.html', context)
    #return redirect(reverse('home'))
    

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'xchange/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'xchange/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        first_name=form.cleaned_data['firstname'],\
                                        last_name=form.cleaned_data['lastname'],\
                                        password=form.cleaned_data['password1'])
    new_user.save()
    profile = Profile(profile_user=new_user, age=0, bio="")
    profile.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))


def photo(request, id):
    item = get_object_or_404(Profile, id=id)
    if not item.photo:
        raise Http404

    return HttpResponse(item.photo, content_type=item.content_type)


def get_post_json(request):
    items = Item.objects.all().order_by('-time')
    tempList = []
    for item in items:
        tempList.append({"itemid":item.id, 
            "time":str(item.time), 
            "username":item.user.profile_user.username, 
            "userid":item.user.profile_user.id,
            "text":item.text})
    response_text = json.dumps(tempList) #dump list as JSON
    return HttpResponse(response_text, content_type='application/json')


@login_required
@csrf_exempt
def comment(request, id):
    postid = id
    # tempuser = request.user.profile_user
    print request.POST['content']
    new_comment = Comment(comment=request.POST['content'],\
                        user=request.user.profile,\
                        item=get_object_or_404(Item, id=id))
    new_comment.save()
    comments = new_comment.item.comment_set.all().order_by('time')
    tempList = []
    for comment in comments:
        tempList.append({
            "time":str(comment.time), 
            "username":comment.user.profile_user.username, 
            "userid":comment.user.profile_user.id,
            "text":comment.comment})
    # response_text = serializers.serialize('json',tempList)
    response_text = json.dumps(tempList) #dump list as JSON
    #return render(request, 'xchange/home.html', context)
    return HttpResponse(response_text, content_type='application/json')

@login_required
def comment_form(request, id):
    new_comment = Comment(comment=request.POST['content'],\
                        user=request.user.profile,\
                        item=get_object_or_404(Item, id=id))
    new_comment.save()
    return redirect(reverse('home'))






    
