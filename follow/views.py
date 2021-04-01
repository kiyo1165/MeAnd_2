from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from .models import Follow
from plan.models import Plan
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.

def FollowView(request, pk):
    print(request, pk)
    if request.method == "POST":
        plan_set_user = Plan.objects.get(pk=pk)
        follower_user = get_object_or_404( User, pk=plan_set_user.user.pk )  # フォローされるユーザー
        follow_user = request.user  # フォローするユーザー
        try:
            follow = Follow.objects.filter(follower_user=follow_user)
            if follow.exists():
                follow.delete()
                messages.warning(request, f'{follower_user.first_name}さんのフォローを解除しました。')
            else:
                follow.create( follow_user=follower_user, follower_user=follow_user)
                messages.info(request, f'{follower_user.first_name}さんをフォローしました。')
        except:
            return redirect( '/accounts/login/')
    return redirect('main:plan_detail', pk=pk)
