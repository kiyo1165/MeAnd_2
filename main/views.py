from django.shortcuts import get_object_or_404,redirect, render
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from category.models import Category
from plan.models import Plan
from accounts.models import Qualification, User, Profile
from message.form import MessageForm
from accounts.models import User
from message.models import Message
from django.db.models import Q
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from follow.models import Follow


# Create your views here.
class CateSearch(TemplateView):
    model = Category, Plan
    template_name = 'main/category_index.html'

    def get_context_data(self, **kwargs):
        ctx = super(CateSearch, self).get_context_data()
        ctx['objects'] = Category.objects.all()
        return ctx


class CateSearchDone(TemplateView):
    model = Plan
    template_name = 'main/category_search_done.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        detail_data = Category.objects.get(name=self.kwargs['name'])
        plan_list = Plan.objects.filter(category=detail_data.id)
        ctx = {
            'detail_data': detail_data,
            'plan_list': plan_list,
        }
        return ctx


class QualificationSearch(TemplateView):
    model = Qualification
    template_name = 'main/qualification_index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['objects'] = Qualification.objects.all()
        return ctx


class QualificationSearchDone(ListView):
    model = Profile
    template_name = 'main/qualification_search_done.html'
    slug_field = 'qualification_name'
    slug_url_kwarg = 'qualification_name'

    def get_context_data(self, **kwargs):
        profile_list = Profile.objects.filter(qualification__qualification_name=self.kwargs['qualification_name'])
        ctx = {
            'profile_list': profile_list,
        }
        return ctx


class ConsList(ListView):
    model = User
    template_name = 'main/cons_list.html'

class ConsDetail(DetailView):
    model = User
    template_name = 'main/cons_detail.html'


class DetailSendMessage(CreateView):
    model = Message
    template_name = 'message/message_create.html'
    form_class = MessageForm

    def form_valid(self, form):
        user_2 = get_object_or_404(User, pk=self.request.user.pk)
        form = form.save(commit=False)
        form.user_2 = user_2
        self_plan = Plan.objects.get(pk=self.kwargs['pk'])
        form.user = User.objects.get(pk=self_plan.user_id)
        form.save()
        return redirect('message:message_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_2 = self.request.user.id
        self_plan = Plan.objects.get( pk=self.kwargs['pk'] )
        user = User.objects.get( pk=self_plan.user_id )
        ctx['message_list'] = Message.objects.filter(Q(user_2=user_2, user=user) | Q(user=user_2, user_2=user)).order_by('-created_at')
        ctx['message_receiver'] = User.objects.get(pk=self_plan.user_id)
        return ctx

class PlanDetail(DetailView, DetailSendMessage):
    model = Plan
    template_name = 'main/plan_detail.html'

    def form_valid(self, form):
        user_2 = get_object_or_404(User, pk=self.request.user.pk)
        form = form.save(commit=False)
        form.user_2 = user_2
        self_plan = Plan.objects.get(pk=self.kwargs['pk'])
        form.user = User.objects.get(pk=self_plan.user_id)
        form.save()
        return redirect('main:cate_search')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if  self.request.user.is_anonymous:
            ctx['self_category_list'] = Plan.objects.filter( category=self.object.category_id )
            return ctx
        elif Follow.objects.filter(follower_user=self.request.user):
            follow_check = True
        else:
            follow_check = False
        ctx['follow_check'] = follow_check
        ctx['self_category_list'] = Plan.objects.filter(category=self.object.category_id)
        return ctx


class UserList(TemplateView):
    template_name = 'main/user_list.html'

def UserListJson(request):
    users = serialize('json', User.objects.all())
    # follow_list = []
    # for user in users:
    #     followed = print(type(user.follow_user.filter(follower_user=request.user)))
    #     followed = str(followed)
    #     if followed.exists():
    #         follow_list.append(user)
    return  JsonResponse(users, safe=False)

# render(request, 'main/user_list.html', context)


# context = {
    #     'users':users,
    #     'follow_list':follow_list,
    # }


