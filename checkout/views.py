from django.views.generic import ListView, TemplateView, UpdateView, DetailView
from .models import CheckOutList
from .forms import CheckOutForm
from django.urls import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
import stripe

class ContractList(ListView):
    model = CheckOutList
    template_name = 'checkout/contract_list.html'

    def get_queryset(self):
        queryset = CheckOutList.objects.filter(vendor_user=self.request.user)
        return queryset


class BuyerSideContractList(ListView):
    model = CheckOutList
    template_name = 'checkout/buyer_side_contract_list.html'
    form_class = CheckOutForm

    def get_queryset(self):
        queryset = CheckOutList.objects.filter(buyer_user=self.request.user)
        return queryset


def contract_cancel(request, pk):
    check = get_object_or_404(CheckOutList, pk=pk)
    form = CheckOutForm(request.POST or None, instance=check)

    if request.method == 'POST' and form.is_valid():
        form = form.save(commit=False)
        form.cancel_flag = True
        form.save()
        messages.info(request, f'{check.plan.title}のキャンセルが完了しました。メールをご確認ください。')
        stripe.Refund.create(
            charge=check.strip_id,
            amount=check.amount,
        )
        return redirect('checkout:buyer_contract_list')

    ctx = {
        'check': check
    }

    return render(request, 'checkout/buyer_side_contract_list.html',ctx )






      




















