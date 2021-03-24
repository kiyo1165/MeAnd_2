from django.shortcuts import get_object_or_404,redirect, render
from django.views.generic import TemplateView, DetailView, CreateView
from category.models import Category
from plan.models import Plan
from message.form import MessageForm
from accounts.models import User
from message.models import Message
from django.db.models import Q
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

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


