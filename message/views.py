from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import Message
from .form import MessageForm
from accounts.models import User
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import datetime


# class OnlyYouMixin(UserPassesTestMixin):
#     raise_exception = True
#
#     # request.user と Planモデルと紐付いているuserprofile.user_idを真偽値としている。
#     def test_func(self, **kwargs):
#         user = self.request.user
#         if not user.is_anonymous:
#             return user.pk == self.request.user.userprofile.user_id


class SendMessage(CreateView):
    model = Message
    template_name = 'message/message_create.html'
    form_class = MessageForm

    def form_valid(self, form):
        user_2 = get_object_or_404(User, pk=self.request.user.pk)
        form = form.save(commit=False)
        form.user_2 = user_2
        form.user = User.objects.get(pk=self.kwargs['pk'])
        form.save()
        return redirect('message:message_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_2 = self.request.user.id
        user = self.kwargs['pk']
        ctx['message_list'] = Message.objects.filter(Q(user_2=user_2, user=user) | Q(user=user_2, user_2=user)).order_by('-created_at')
        ctx['message_host'] = User.objects.get(pk=self.kwargs['pk'])
        return ctx


class MessageList(ListView):
    model = Message
    template_name = 'message/message_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(user_2=user).order_by('-created_at')
        queryset_2 = Message.objects.filter(user=user).order_by('-created_at')
        # ② distinctという重複を削除するDjangofilterが存在するが、癖があるので自作で重複を削除するのをオススメ
        exists_user_list = []
        distinct_list = []

        message_list = []
        message_list2 = []

        for message_obj in queryset:
            message_elm = {
                'id': message_obj.id,
                'user': message_obj.user,
                'send_text': message_obj.send_text,
                'created_at': message_obj.created_at
            }
            message_list.append(message_elm)

        for message_obj in queryset_2:
            message_elm = {
                'id': message_obj.id,
                'user': message_obj.user_2,
                'send_text': message_obj.send_text,
            }
            message_list2.append(message_elm)

            chat_list = message_list + message_list2

            for message_obj in chat_list:
                if message_obj['user'] not in exists_user_list:
                    distinct_list.append( message_obj )
                    exists_user_list.append( message_obj['user'] )
                    print(distinct_list)
            return distinct_list

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     today_now =  datetime.dateteime.time()
    #     user_2 = self.request.user
    #
    #     return