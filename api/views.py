from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow, Dweet, Like, Comment
from django.db.models import Q
from django.contrib import messages


# Create your views here.
@csrf_exempt
@login_required
def hello(request):
    if request.method == 'GET':
        profile = Profile.objects.get(user=request.user)
        followed = Follow.objects.filter(user=request.user)
        followed_users = list(x.follow_user for x in followed)
        followed_dweets = list(Dweet.objects.filter(Q(user__in=followed_users) | Q(user=request.user)).order_by("-created_at"))
        print(followed_dweets)
        all_profiles = list(Profile.objects.all())
        dweet_ids_liked_by_profile = list(Like.objects.filter(profile=profile).values_list('dweet__id', flat=True))
        print(dweet_ids_liked_by_profile)
        return render(request, 'home.html', {"dweets": followed_dweets, "all_profiles": all_profiles, "dweet_ids_liked_by_profile": dweet_ids_liked_by_profile})


@csrf_exempt
@login_required
def dweet_detail(request, id):
    dweet = Dweet.objects.get(pk=id)
    dweet_likes = Like.objects.filter(dweet_id=id)
    dweet_comments = Comment.objects.filter(dweet_id=id)
    is_liked = Like.objects.filter(Q(profile_id=request.user.profile.id) & Q(dweet_id=id)).first()
    if is_liked is not None:
        is_liked = True
    else:
        is_liked = False
    return render(request, 'dweet_detail.html', {"dweet": dweet, "dweet_likes": dweet_likes, "dweet_comments": dweet_comments, "is_liked": is_liked})


@csrf_exempt
@login_required
def follow(request, id):
    profile_to_follow = Profile.objects.get(pk=id)
    follow = Follow.objects.filter(Q(user=request.user) & Q(follow_user=profile_to_follow.user)).first()
    if follow is None:
        follow = Follow(user=request.user, follow_user=profile_to_follow.user)
        follow.save()
    else:
        messages.error(request, f"Already following the user- {profile_to_follow.user.username}")
    return redirect("profile", id=id)


@csrf_exempt
@login_required
def unfollow(request, id):
    profile_to_unfollow = Profile.objects.get(pk=id)
    follow = Follow.objects.filter(Q(user=request.user) & Q(follow_user=profile_to_unfollow.user)).first()
    if follow is not None:
        follow.delete()
    else:
        messages.error(request, f"You are not following the user- {profile_to_unfollow.user.username}")
    return redirect("profile", id=id)

@csrf_exempt
@login_required
def add_dweet(request):
    if request.method == 'POST':
        dweet_body = request.POST['dweet_body']
        dweet = Dweet(user=request.user, body=dweet_body)
        dweet.save()
        return redirect("/")


@csrf_exempt
@login_required
def delete_dweet(request, id=None):
    if request.method == 'GET' and id is not None:
        dweet_to_delete = Dweet.objects.get(pk=id)
        if dweet_to_delete.user == request.user:
            dweet_to_delete.delete()
            messages.success(request, "Dweet deleted successfully")
        else:
            messages.error(request, "Error deleting dweet. You can only delete your dweets")
        return redirect('home')


@csrf_exempt
@login_required
def get_followed_dweets(request):
    if request.method == 'GET':
        followed = Follow.objects.filter(user=request.user)
        followed_users = list(x.follow_user for x in followed)
        followed_dweets = list(Dweet.objects.filter(Q(user__in=followed_users) | Q(user=request.user)).order_by("-created_at"))
        print(followed_dweets)
        return HttpResponse(followed_dweets)


@csrf_exempt
@login_required
def get_all_dweets(request):
    if request.method == 'GET':
        dweets = list(Dweet.objects.all().order_by("-created_at"))
        return HttpResponse(dweets)


@csrf_exempt
@login_required
def display_profile(request, id=None):
    if request.method == 'GET':

        if id is None or id == request.user.profile.id:
            # Own profile
            profile = Profile.objects.get(user=request.user)
            user = request.user
            owner = True
        else:
            # Other user's profile
            profile = Profile.objects.get(pk=id)
            user = profile.user
            owner = False

        # to check if the user is following this profile
        follow = Follow.objects.filter(Q(user=request.user) & Q(follow_user=profile.user)).first()
        if follow is not None:
            is_following = True
        else:
            is_following = False

        followers = Follow.objects.filter(follow_user=user)
        following = Follow.objects.filter(user=user)
        followers_list = list(f'{x.user.username} ({x.user.email})' for x in followers)
        following_list = list(f'{x.follow_user.username} ({x.follow_user.email})' for x in following)
        profile_dweets = list(Dweet.objects.filter(user=user).order_by("-created_at"))
        dweet_ids_liked_by_profile = list(Like.objects.filter(profile=request.user.profile).values_list('dweet__id', flat=True))

        return render(request, 'profile.html', {"profile": profile, "followers_list": followers_list, "following_list": following_list, "profile_dweets": profile_dweets, "owner": owner, "is_following":is_following, "dweet_ids_liked_by_profile": dweet_ids_liked_by_profile})


@csrf_exempt
@login_required
def like_unlike_dweet(request, id):
    like = Like.objects.filter(Q(dweet_id=id) & Q(profile_id=request.user.profile.id)).first()
    print(like)
    print(request)
    if like is None:
        like = Like(dweet_id=id, profile_id=request.user.profile.id)
        like.save()
    else:
        like.delete()
    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
@login_required
def add_comment(request, id):
    if request.method == "POST":
        comment_body = request.POST['comment_body']
        comment = Comment(body=comment_body, dweet_id=id, profile_id=request.user.profile.id)
        comment.save()
        messages.success(request, "Comment added successfully")
        return redirect(request.META['HTTP_REFERER'])
