from django.urls import path

from .views import ContractList, BuyerSideContractList,contract_cancel

app_name = 'checkout'
urlpatterns = [
    path('contract_list/', ContractList.as_view(), name='contract_list'),
    path('contract_list_buyer/', BuyerSideContractList.as_view(), name='buyer_contract_list'),
    path('contract_list_buyer/<int:pk>/cancel', contract_cancel, name='checkout_cancel'),
]