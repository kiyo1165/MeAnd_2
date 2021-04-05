from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url


# class CustomRedirect(DefaultAccountAdapter):
#
#     def get_login_redirect_url(self, request):
#         url = request.GET.get('next', '')
#         return url