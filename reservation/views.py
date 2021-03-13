import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from .models import  Reservation
from accounts.models import User
from plan.models import Plan

class UserList(ListView):
    model = User
    template_name = 'reservation/user_list.html'

class PlanList(ListView):
    model = Plan
    template_name = 'reservation/plan_list.html'

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
        user = User.objects.get(pk=self.request.user.id)
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
        for hour in range(9, 18):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row

        start_time = datetime.datetime.combine(start_day, datetime.time(hour=9, minute=0, second=0))
        end_time =datetime.datetime.combine(end_day, datetime.time(hour=17, minute=0, second=0))
        for schedule in Reservation.objects.filter( staff=user ).exclude(
                Q( start__gt=end_time ) | Q( end__lt=start_time ) ):
            local_dt = timezone.localtime( schedule.start )
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                calendar[booking_hour][booking_date] = False

        context['user'] = user
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta( days=7 )
        context['next'] = days[-1] + datetime.timedelta( days=1 )
        context['today'] = today
        context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context
