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
    posts = Post.objects.all().order_by('-created_on')
    print(posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj[0])
    form = NewPostForm()
    current_user = request.user
    
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
    try:
        user_profile = get_object_or_404(Profile, user=user)
        return render(request, "network/index.html", {
            'posts': page_obj,
            'form': form,
            "user_profile": user_profile,
            "page_user": current_user.id
        })
    except:
        return HttpResponseRedirect('login')
    

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
    active_user = request.user
    get_user_object = get_object_or_404(User, username=user)
    profile = get_object_or_404(Profile, user=get_user_object)
    active_user_profile = get_object_or_404(Profile, user=active_user)
    page_user_object = get_object_or_404(User, username=active_user)
    follow_status = page_user_object in profile.following.all()
    posts = Post.objects.filter(author__slug=user)

    return render(request, "network/profile.html", {
        'posts' : posts,
        'active_user': active_user,
        'profile' : profile,
        'followers': profile.followers,
        'followings': profile.following,
        "active_user": active_user,
        "get_user_object": get_user_object,
        "active_user_profile": active_user_profile,
        "user_profile" : active_user_profile,
        "follow_status": follow_status,
    })

def following_posts(request, user):
    #get the user's profile
    get_user_object = get_object_or_404(User, username=user)
    get_profile = get_object_or_404(Profile, user=get_user_object)

    #get the profile of people that the user follows
    user_following = get_profile.following.all() #Users following
    profiles = Profile.objects.filter(user__in = user_following)

    # Get posts from profile that user follows
    posts = Post.objects.filter(author__in= profiles).order_by('-created_on')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_profile = get_object_or_404(Profile, user=request.user)
    
    return render(request, 'network/following_posts.html', {
        'profiles_following': user_following,
        'posts': page_obj,
        'paged_posts': page_obj,
        'user_profile': user_profile
    } )

@login_required
def like(request, id):
    post = get_object_or_404(Post, id=id)
    data = serializers.serialize("json", Post.objects.filter(id=id), fields=('body','liked'))
    try:
        user_profile = Profile.objects.get(user=request.user)
        post_liked_list = post.liked.all()
        print(post_liked_list)
        

        if user_profile not in post_liked_list:
            post.liked.add(user_profile)
            post.save()
            print(f'These are the profiles that have liked this post: {post.liked.all()}')
            updated_data = serializers.serialize("json", Post.objects.filter(id=id), fields=('body','liked'))
            return JsonResponse({"liked": True, 
                                 "data": data,
                                 "updated_data": updated_data})

        else:
            post.liked.remove(user_profile)
            post.save()
            print(f'These are the profiles that have liked this post: {post.liked.all()}')
            data = serializers.serialize("json", Post.objects.filter(id=id), fields=('body','liked'))
            updated_data = serializers.serialize("json", Post.objects.filter(id=id), fields=('body','liked'))
            return JsonResponse({"liked": False, 
                                 "data": data,
                                 "updated_data": updated_data})

    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('login'))
    

def follow(request, user):
    active_user = request.user
    print(f'Current Profile being viewed is {user}')
    
    try:
        user_object = get_object_or_404(User, username=active_user)
        user_profile = get_object_or_404(Profile, user=active_user)
        user_to_follow = get_object_or_404(User, username=user)
        user_to_follow_profile = get_object_or_404(Profile, user=user_to_follow)
        data = serializers.serialize( "json", Profile.objects.filter(user=active_user), fields=('users', 'followers', 'following'))
        if user_to_follow != user_profile.user:
            if user_to_follow not in user_profile.following.all():
                user_profile.following.add(user_to_follow)
                user_to_follow_profile.followers.add(user_object)
                user_profile.save()
                user_to_follow_profile.save()
                return JsonResponse({"following": "True", 'data': data})
            else:
                user_profile.following.remove(user_to_follow)
                user_to_follow_profile.followers.remove(user_object)
                user_profile.save()
                user_to_follow_profile.save()
                return JsonResponse({"following": "False", 'data': data})
                
        return JsonResponse({"error":"Own Profile can not be followed"})
    except Profile.DoesNotExist:
        return JsonResponse({"error" : "Profile does not exists"})

  
        
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
