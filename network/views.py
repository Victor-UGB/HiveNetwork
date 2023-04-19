import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core import serializers
from django.core.paginator import Paginator 
from .forms import *

from .models import User, Post


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = NewPostForm()
    current_user = request.user
    # profile = get_object_or_404(Profile, user=current_user)


    # print(f'This is the user now {current_user}')
    # print(f'This is the proile now {profile} {profile.user.username}')
    # print(current_user.id)
    # print(Post.objects.filter(id=1))
    # print(f'Current Profile is {profile.user.id}')
    
    if request.method == "POST":
        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        form = NewPostForm(request.POST)

        if form.is_valid():
            full_form = form.save(commit=False)
            full_form.author = user_profile
            full_form.save()

            return HttpResponseRedirect(reverse("index"))
            
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    return render(request, "network/index.html", {
        'posts' : page_obj,
        'form' : form,
        "user_profile": user_profile,
        "page_user": current_user.id
    })

    

def save_edit(request, id):

    print("running")

    #Query for Request object
    try:
        post = Post.objects.get(id=id)
        print(post)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Handle update 

    if request.method == "POST":
        post_edit = request.POST["post-edit"]

        if post_edit is not None:
            post.body = post_edit

            post.save()

            return HttpResponseRedirect(reverse("index"))
        return JsonResponse({"error": "Edit failed."}, status=404)
    
    return JsonResponse({'error': "Invalid request"}, status =400 )

        

def profile(request, user):
    # filter post that were created by user

    page_user = request.user
    get_user_object = get_object_or_404(User, username=user)
    profile = get_object_or_404(Profile, user=get_user_object)
    posts = Post.objects.filter(author__slug=user)

    print(f'This is the {page_user.id}')
    print(f'This is {profile.id}\'s profile')
    return render(request, "network/profile.html", {
        'posts' : posts,
        'user' : profile.user,
        'followers': profile.followers,
        'followings': profile.following,
        "page_user": page_user.id
    })

def following_posts(request, user):
    #get the user and user's profile
    get_user_object = get_object_or_404(User, username=user)
    print(get_user_object)
    get_profile = get_object_or_404(Profile, user=get_user_object)
    print(get_profile)

    #get the people that the user follows
    profile_following = get_profile.following.all()
    all_post  = Post.objects.all()
    print(all_post)

    first_profile = profile_following[0]
    print(profile_following)
    print(first_profile)
    first_profile_obj = Profile.objects.filter(user=first_profile)
    print(first_profile_obj)
    first_profile_posts = Post.objects.filter(author=first_profile_obj[0])
    print(first_profile_posts)

    select_profiles = [i for i in profile_following]
    print(select_profiles)
    p = [ i.slug for i in select_profiles]
    print(p)
    select_posts = [i for i in all_post if i.author != None and i.author.user.slug in p]

    print(select_posts)



    

    # for i in all_post:
    #     # if i.author in profile_following:
    #     select_posts.update(i)
    
        # print(select_posts)


    return render(request, 'network/following_posts.html', {
        'profiles_following': profile_following,
        'posts': select_posts
    } )
    #get the post of the 'followings'

@login_required
def like(request, id):
    post = get_object_or_404(Post, id=id)
    data = serializers.serialize("json", Post.objects.filter(id=id), fields=('body','liked'))

    try:
        user_profile = Profile.objects.get(user=request.user)
        post_liked_list = post.liked.all()
        

        if user_profile not in post_liked_list:

            post.liked.add(user_profile)
            post.save()
            print(f'These are the profiles that have liked this post: {post.liked.all()}')
            return JsonResponse({"liked": False, "data": data})

        else:
            
            post.liked.remove(user_profile)
            post.save()
            print(f'These are the profiles that have liked this post: {post.liked.all()}')
            return JsonResponse({"liked": True, "data": data})

        print(f'These are the profiles that have liked this post after change: {post.liked.all()}')

        return HttpResponseRedirect(reverse('index'))

    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('login'))
    



    # user_profile = get_object_or_404(Profile, user=request.user)

    # check if user is logged in

        # check if user_profile has liked the profile

            # add profile to list of liked profile

            # remove profile from liked profile

        # save user_profile
        # return jsonResponse

        
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    data = serializers.serialize('json',post)

    try:
        return JsonResponse({'post': data})
    except Post.DoesNotExist:
        return JsonResponse("Post does not exist")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
