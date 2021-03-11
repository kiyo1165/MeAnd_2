from django.shortcuts import render, get_object_or_404, redirect

from .models import Plan
from accounts.models import User
from django.views.generic import DetailView
from .form import PlanForm
from django.contrib import messages
# Create your views here.

def PlanCreate(request):
    user = get_object_or_404(User, pk=request.user.id )
    plan_form = PlanForm(request.POST or None)
    if request.method == 'POST' and  plan_form.is_valid():
        form = plan_form.save(commit=False)
        form.user = user
        form.save()
        plan_form.save_m2m()
        messages.success(request, f'プランを登録しました。')
        return redirect('main:cate_search')
    else:
        ctx = {
            'plan_form':plan_form,
        }
        return render(request, 'plan/plan_create.html', ctx)

class PlanDetail(DetailView):
    model = Plan
    template_name = 'plan/plan_detail.html'
