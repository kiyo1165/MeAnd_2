import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView
from .models import  Reservation, ReservationMessage
from accounts.models import User
from plan.models import Plan
from django.contrib import messages
from .form import BookingForm
#パーミッション
from django.contrib.auth.mixins import LoginRequiredMixin
from plan.models import StyleChoices


class UserList(ListView):
    model = User
    template_name = 'reservation/user_list.html'

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = self.user
        return ctx

    def get_queryset(self):
        user = self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        queryset = super().get_queryset().filter(user=user)
        return queryset

class StaffCalendar(TemplateView):
    template_name = 'reservation/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan = Plan.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(pk=plan.user.id)
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)

        else:
            base_date = today

        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(9, 23):
            row = {}

            for day in days:
                row[day] = True
            calendar[hour] = row



        start_time = datetime.datetime.combine(start_day, datetime.time(hour=9, minute=0, second=0))
        end_time =datetime.datetime.combine(end_day, datetime.time(hour=23, minute=0, second=0))
        for schedule in Reservation.objects.filter( user2=user ).exclude(
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


class Booking(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'reservation/booking.html'
    form_class = BookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context['staff'] = get_object_or_404( Plan, pk=self.kwargs['pk'] )
        return context

    def form_valid(self, form):
        plan = get_object_or_404( Plan, pk=self.kwargs['pk'] )
        user = User.objects.get( pk=self.request.user.id )
        user_2 = User.objects.get(pk=plan.user.pk)
        year = self.kwargs.get( 'year' )
        month = self.kwargs.get( 'month' )
        day = self.kwargs.get( 'day' )
        hour = self.kwargs.get( 'hour' )
        start = datetime.datetime( year=year, month=month, day=day, hour=hour )
        end = datetime.datetime( year=year, month=month, day=day, hour=hour + 1 )
        if Reservation.objects.filter( user2=user_2, start=start ).exists():
            messages.error( self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。' )
        else:
            schedule = form.save( commit=False )
            schedule.user = user
            schedule.user2 = user_2
            schedule.plan = plan
            schedule.start = start
            schedule.end = end
            schedule.save()
            form.save_m2m()
            messages.success( self.request,'予約が完了しました。登録されているメールアドレスをご確認ください。')

            return redirect( 'reservation:next_calendar', pk=plan.pk, year=year, month=month, day=day )


class BookingMessage(CreateView):
    model = ReservationMessage
    template_name = 'reservation/booking_message.html'
    fields = ('message',)

    
    def form_valid(self, form):
        form = form.save(commit=False)
        reservation = Reservation.objects.get(pk=self.kwargs['pk'])
        user = get_object_or_404(User, pk=self.request.user.pk)
        form.reservation = reservation
        form.user = user
        form.save()
        return redirect('accounts:reservation_list')

    def get_context_data(self, **kwargs):
        ctx = super(BookingMessage, self).get_context_data()
        reservation = Reservation.objects.get(pk=self.kwargs['pk'])
        booking_message = ReservationMessage.objects.filter(reservation=self.kwargs['pk']).order_by('-created_at')
        ctx['reservation_message'] = reservation
        ctx['booking_message'] = booking_message
        return ctx
        
