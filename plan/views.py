from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Plan
from accounts.models import User
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from .form import PlanForm
from django.contrib import messages
# Create your views here.

def PlanCreate(request):
    user = get_object_or_404(User, pk=request.user.id )

    plan_form = PlanForm(request.POST or None)
    if request.method == 'POST' and  plan_form.is_valid():
        form = plan_form.save(commit=False)
        form.user = user
        print(request)
        form.plan_sign = request.FILES.get('plan_sign')
        print(form.plan_sign)
        form.save()
        plan_form.save_m2m()
        messages.success(request, f'プランを登録しました。')
        return redirect('plan:plan_list')
    else:
        print('error')
        ctx = {
            'plan_form':plan_form,
        }
        return render(request, 'plan/plan_create.html', ctx)

class PlanList(ListView):
    model = Plan
    template_name = 'plan/plan_list.html'

    def get_queryset(self):
        user = self.request.user.pk
        queryset = Plan.objects.filter(user=user)
        return queryset

class MyPagePlanDetail(DetailView):
    model = Plan
    template_name = 'plan/mypage_plan_detail.html'

def MyPagePlanUpdate(request, pk):
    user = get_object_or_404( User, pk=request.user.id )
    plan = get_object_or_404(Plan, pk=pk)
    plan_form = PlanForm( request.POST or None, instance=plan )
    if request.method == 'POST' and plan_form.is_valid():
        form = plan_form.save( commit=False )
        form.user = user
        form.save()
        plan_form.save_m2m()
        messages.success( request, f'プランを登録しました。' )
        return redirect( 'plan:plan_list' )
    else:
        ctx = {
            'plan_form': plan_form,
        }
        return render( request, 'plan/plan_create.html', ctx )


class MyPagePlanDelete(DeleteView):
    model = Plan
    success_url = reverse_lazy('plan:plan_list')
