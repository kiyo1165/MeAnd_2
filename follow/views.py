from django.shortcuts import render, get_object_or_404
from accounts.models import User
from .models import Follow
from django.http import JsonResponse

# Create your views here.


def FollowView(request):
    if request.method =="POST":
        follow_user = get_object_or_404(User, pk=request.POST.get('user.pk'))
        user = request.user
        followed = False
        follow = Follow.objects.filter(follow_user=follow_user, user=user)
        if follow.exists():
            follow.delete()
        else:
            follow.create(follow_user=follow, user=user)
            followed = True

        context={
            'user_id': user.id,
            'followed': followed,
            'count': user.follower_user.count(),
        }

    if request.is_ajax():
        return JsonResponse(context)