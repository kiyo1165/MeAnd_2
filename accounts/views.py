from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from .models import Profile
from .forms import UserForm, ProfileForm, ReserveUpdateForm
from .models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from plan.models import Plan

#パーミッション
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.urls import reverse_lazy, reverse

import datetime
from django.utils import timezone
from reservation.models import Reservation
from django.db.models import Q
from django.conf import settings
from accounts.models import CounselorRegister
from django.core.mail import send_mail



class OnlyStaffMixin( UserPassesTestMixin ):
    raise_exception = True

    def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user == self.request.user or self.request.user.is_superuser


class OnlyMyPageMixin( UserPassesTestMixin ):
    raise_exception = True

    def test_func(self):
        user = get_object_or_404(User,pk=self.request.user.id)
        return user


def ProfileEdit(request):
    user = User.objects.get( pk=request.user.pk )
    profile = get_object_or_404( Profile, user_id=request.user.pk )
    user_form = UserForm( request.POST or None, instance=user )
    profile_form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form = user_form.save( commit=False )
        user_form.save()
        profile_form = profile_form.save( commit=False )
        if request.FILES.get( 'face_image' ) is None:
            profile_form.face_image = profile.face_image
            profile_form.user = user
            profile_form.save()
            messages.success( request, f'正常に登録されました' )
            return redirect( 'accounts:mypage' )
        else:
            profile_form.face_image = request.FILES.get( 'face_image' )
            profile_form.user = user
            profile_form.save()
            messages.success( request, f'正常に登録されました' )
            return redirect( 'accounts:mypage' )
    else:
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }
        return render( request, 'accounts/profile_form.html', ctx )


class MyPage(TemplateView):
    model = Profile
    template_name = 'accounts/my_page.html'

    def get_context_data(self, **kwargs):
        ctx = super( MyPage, self ).get_context_data(**kwargs)
        plan = Plan.objects.filter( user_id=self.request.user.id )
        user = User.objects.get( pk=self.request.user.pk )
        ctx['my_page'] = Profile.objects.get( user_id=user )
        ctx['plan_list'] = Plan.objects.filter( user_id=user )
        return ctx


class MyPageCalendar(TemplateView):
    template_name = 'accounts/my_page_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        user = get_object_or_404(User, pk=self.request.user.pk)
        plan = Plan.objects.filter(user_id=user)
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get( 'year' )
        month = self.kwargs.get( 'month' )
        day = self.kwargs.get( 'day' )
        if year and month and day:
            base_date = datetime.date( year=year, month=month, day=day )

        else:
            base_date = today

        week = [base_date + datetime.timedelta( days=day ) for day in range( 7 )]
        start_day = week[0]
        end_day = week[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range( 9, 23 ):
            row = {}
            for day in week:
                row[day] = True
            calendar[hour] = row



        start_time = datetime.datetime.combine( start_day, datetime.time( hour=9, minute=0, second=0 ) )
        end_time = datetime.datetime.combine( end_day, datetime.time( hour=23, minute=0, second=0 ) )
        for schedule in Reservation.objects.filter(user2=self.request.user.id).exclude(
                Q( start__gt=end_time ) | Q( end__lt=start_time ) ):
            local_dt = timezone.localtime( schedule.start )

            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                calendar[booking_hour][booking_date] = False

        context['plan'] = plan
        context['calendar'] = calendar
        context['week'] = week
        context['hour'] = hour
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = week[0] - datetime.timedelta( days=7 )
        context['next'] = week[-1] + datetime.timedelta( days=1 )
        context['today'] = today
        context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context

class GuestMyPageConsList(TemplateView):
    model = User
    template_name = 'accounts/guest/guest_my_page_conslist.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        cons = User.objects.filter(is_staff=True, is_superuser=False)
        ctx['cons_list'] = cons
        return ctx

class FollowList(TemplateView):
    model = User
    template_name = 'accounts/follow_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        user = User.objects.get( pk=self.request.user.id )
        ctx['follow_list'] = user.follower_user.all()
        return ctx


class MyPageMixin(MyPageCalendar,GuestMyPageConsList, FollowList):
    template_name = 'accounts/index.html'
    model = Plan
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        plan = Plan.objects.filter( user_id=self.request.user.id )
        user = get_object_or_404(User, pk=self.request.user.pk )
        ctx['my_page'] = Profile.objects.get( user_id=user )
        ctx['plan_list'] = Plan.objects.filter( user_id=user )
        return ctx


class MyProfile( TemplateView ):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super( MyProfile, self ).get_context_data()
        ctx['my_page'] = Profile.objects.get( user_id=self.request.user.id )
        return ctx

#TODO 詳細ページのリンク確認
class MyPageSchedule(UpdateView):
    model = Reservation
    # fields = ('start', 'end', 'message')
    form_class = ReserveUpdateForm
    template_name = 'accounts/schedule_form.html'
    success_url = reverse_lazy('accounts:mypage')

    def form_valid(self, form):
        messages.success(self.request, f'更新しました。')
        return super(MyPageSchedule, self).form_valid(form)


class MyPageDayDetail(TemplateView ):
    template_name = 'accounts/my_page_day_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = get_object_or_404( User, pk=self.request.user.pk )
        year = self.kwargs.get( 'year' )
        month = self.kwargs.get( 'month' )
        day = self.kwargs.get( 'day' )
        date = datetime.date( year=year, month=month, day=day )

        # 9時から17時まで1時間刻みのカレンダーを作る
        calendar = {}
        for hour in range(9, 23):
            calendar[hour] = []

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine( date, datetime.time( hour=9, minute=0, second=0 ) )
        end_time = datetime.datetime.combine( date, datetime.time( hour=23, minute=0, second=0 ) )
        for schedule in Reservation.objects.filter( user2=self.request.user.pk ).exclude(
                Q( start__gt=end_time ) | Q( end__lt=start_time ) ):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar:
                calendar[booking_hour].append( schedule )

        context['calendar'] = calendar
        context['plan'] = user
        return context


class MyPageScheduleDelete(DeleteView):
    model = Reservation

    def form_valid(self, form):
        messages.warning(self.request, f'削除しました。')
        return super(MyPageSchedule, self).form_valid(form)

    def get_success_url(self):
        return reverse('accounts:mypage')


@require_POST
def my_page_holiday_add(request, pk, year, month, day, hour):
    user = User.objects.get(pk=pk)
    if user == request.user or request.user.is_superuser:
        start = datetime.datetime( year=year, month=month, day=day, hour=hour )
        end = datetime.datetime( year=year, month=month, day=day, hour=hour + 1 )
        Reservation.objects.create( user2=user,user=user, start=start, end=end, message='休暇(システムによる追加)', active=False )
        return redirect( 'accounts:my_page_day_detail', pk=pk, year=year, month=month, day=day )



def my_page_day_holiday_add(request, pk, year, month, day):
    user = User.objects.get(pk=pk)
    if user == request.user or request.user.is_superuser:
        for i in range(9,23):
            start = datetime.datetime( year=year, month=month, day=day, hour=i )
            end = datetime.datetime( year=year, month=month, day=day, hour=i +1 )
            Reservation.objects.create( user2=user,  start=start, end=end, message='休暇(システムによる追加)', active=False )
        return redirect( 'accounts:mypage' )



def my_page_day_holiday_delete(request, pk, year, month, day):
    user = User.objects.get(pk=pk)
    if user == request.user or request.user.is_superuser:
        for i in range(9,23):
            start = datetime.datetime( year=year, month=month, day=day, hour=i )
            end = datetime.datetime( year=year, month=month, day=day, hour=i +1 )
            Reservation.objects.filter(user2=pk, start=start, end=end).delete()
        return redirect( 'accounts:mypage' )





class CounselorGuidance(TemplateView):
    template_name = 'accounts/counselor_guidance.html'


class CounselorRegister(OnlyStaffMixin, CreateView):
    template_name = 'accounts/counselor_register.html'
    model = CounselorRegister
    fields = ('identification', 'credentials', 'signature', 'address', 'agreement')
    success_url = reverse_lazy('accounts:profile_edit')

    def form_valid(self, form):
        register = form.save(commit=False)
        user = User.objects.get( pk=self.kwargs['pk'] )
        register.user = user
        register.save()
        send_mail(
            subject='【カウンセラーの仮登録完了】' + user.last_name + 'さん',
            message=user.last_name + 'さんのカウンセラーの仮登録が完了しました。内容の確認、お手続きの完了まで3〜5営業日頂いております。完了次第メールにてご連絡致します。',
            recipient_list=['admin@example.com', ],
            from_email=user.email
        )
        messages.warning(self.request, f'{user.last_name}{user.first_name}さんのカウンセラーの仮登録が完了しました。確認メールをご確認ください。')
        return super(CounselorRegister, self).form_valid(form)

class CounselorConfirmRegistered(OnlyStaffMixin,TemplateView):
    template_name = 'accounts/conselor_confirm_registered.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cons_object'] = User.objects.get(pk=self.kwargs['pk'])
        return context


class ReservationList(OnlyMyPageMixin, ListView):
    model = Reservation
    template_name = 'accounts/reservation_list.html'

    def get_queryset(self):
        user = self.request.user.pk
        reserve_user = Reservation.objects.filter(Q(user2=user)|Q(user=user),active=True).order_by('-created_at')
        return reserve_user









