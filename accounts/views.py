from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from .models import Profile
from .forms import UserForm, ProfileForm
from .models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from plan.models import Plan
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from reservation.views import StaffCalendar
import datetime
from django.utils import timezone
from reservation.models import Reservation
from django.db.models import Q
from django.conf import settings


class OnlyStaffMixin( UserPassesTestMixin ):
    raise_exception = True

    def test_func(self):
        user = get_object_or_404( User, pk=self.kwargs['pk'] )
        return user == self.request.user or self.request.user.is_superuser


# Create your views here.
def ProfileCreate(request):
    user = User.objects.get( pk=request.user.pk )
    user_form = UserForm( request.POST or None, instance=user )
    profile_form = ProfileForm( request.POST )
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form = user_form.save( commit=False )
        user_form.save()
        profile_form = profile_form.save( commit=False )
        profile_form.face_image = request.FILES.get( 'face_image' )
        profile_form.user = user
        profile_form.save()
        messages.success( request, f'正常に登録されました' )
        return redirect( 'accounts:my_page' )
    else:
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render( request, 'accounts/profile_form.html', ctx )
    #
    # def get_context_data(self, *args, **kwargs):
    #     ctx = super(ProfileCreate, self).get_context_data()
    #     user_form = UserForm()
    #     ctx['user_form'] = user_form
    #     return ctx


def ProfileEdit(request):
    user = User.objects.get( pk=request.user.pk )
    profile = get_object_or_404( Profile, user_id=request.user.pk )
    user_form = UserForm( request.POST or None, instance=user )
    profile_form = ProfileForm( request.POST or None, instance=profile )
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form = user_form.save( commit=False )
        user_form.save()
        profile_form = profile_form.save( commit=False )
        if request.FILES.get( 'face_image' ) is None:
            profile_form.face_image = profile.face_image
            profile_form.user = user
            profile_form.save()
            messages.success( request, f'正常に登録されました' )
            return redirect( 'accounts:my_page' )
        else:
            profile_form.face_image = request.FILES.get( 'face_image' )
            profile_form.user = user
            profile_form.save()
            messages.success( request, f'正常に登録されました' )
            return redirect( 'accounts:my_page' )
    else:
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }
        return render( request, 'accounts/profile_form.html', ctx )


class MyPage( TemplateView ):
    model = Profile
    template_name = 'accounts/my_page.html'

    def get_context_data(self, **kwargs):
        ctx = super( MyPage, self ).get_context_data()
        plan = Plan.objects.filter( user_id=self.request.user.id )
        user = User.objects.get( pk=self.request.user.pk )
        ctx['my_page'] = Profile.objects.get( user_id=user )
        ctx['plan_list'] = Plan.objects.filter( user_id=user )
        # ctx['reservation_list'] = Reservation.objects.filter(plan=)
        return ctx


class MyProfile( TemplateView ):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super( MyProfile, self ).get_context_data()
        ctx['my_page'] = Profile.objects.get( user_id=self.request.user.id )
        return ctx


class MyPageCalendar( StaffCalendar ):
    template_name = 'accounts/my_page_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        plan = Plan.objects.get( pk=self.kwargs['pk'] )
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

        days = [base_date + datetime.timedelta( days=day ) for day in range( 7 )]
        start_day = days[0]
        end_day = days[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range( 9, 23 ):
            row = {}
            for day in days:
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
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta( days=7 )
        context['next'] = days[-1] + datetime.timedelta( days=1 )
        context['today'] = today
        context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context


class MyPageDayDetail( TemplateView ):
    template_name = 'accounts/my_page_day_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        pk = self.kwargs['pk']
        plan = get_object_or_404( Plan, pk=pk )
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
        context['plan'] = plan
        return context


class MyPageSchedule(UpdateView):
    model = Reservation
    fields = ('start', 'end', 'message')
    template_name = 'accounts/schedule_form.html'
    success_url = reverse_lazy('accounts:my_page')

    def form_valid(self, form):
        messages.success(self.request, f'更新しました。')
        return super(MyPageSchedule, self).form_valid(form)




class MyPageScheduleDelete(DeleteView):
    model = Reservation

    def form_valid(self, form):
        messages.success(self.request, f'削除しました。')
        return super(MyPageSchedule, self).form_valid(form)

    def get_success_url(self):
        return reverse('accounts:my_page_schedule', kwargs={'pk':self.kwargs['pk']})


@require_POST
def my_page_holiday_add(request, pk, year, month, day, hour):
    plan = get_object_or_404( Plan, pk=pk )
    if plan.user == request.user or request.user.is_superuser:
        start = datetime.datetime( year=year, month=month, day=day, hour=hour )
        end = datetime.datetime( year=year, month=month, day=day, hour=hour + 1 )
        Reservation.objects.create( plan=plan, start=start, end=end, name='休暇(システムによる追加)' )
        return redirect( 'accounts:my_page_day_detail', pk=pk, year=year, month=month, day=day )

    raise PermissionDenied
