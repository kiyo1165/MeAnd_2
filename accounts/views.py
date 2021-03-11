from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView
from .models import Profile
from .form import UserForm, ProfileForm
from .models import User
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
class ProfileCreate(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_create_form.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.request.user.pk)
        print(form.instance)
        form.instance.user_id = user.id
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        ctx = super(ProfileCreate, self).get_context_data()
        user_form = UserForm()
        ctx['user_form'] = user_form
        return ctx




def ProfileEdit(request):
    user = User.objects.get(pk=request.user.pk)
    profile = get_object_or_404( Profile, user_id=request.user.pk )
    user_form = UserForm( request.POST or None, instance=user)
    profile_form = Profile(request.POST or None, instance=profile)
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form = user_form.save( commit=False)
        user_form.save()
        profile_form = profile_form.save(commit=False )
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




class MyPage(TemplateView):
    model = Profile
    template_name = 'accounts/my_page.html'

    def get_context_data(self, **kwargs):
        ctx = super(MyPage, self).get_context_data()
        ctx['my_page'] = Profile.objects.get(user_id=self.request.user.id)
        return ctx


class MyProfile(TemplateView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super(MyProfile, self).get_context_data()
        ctx['my_page'] = Profile.objects.get(user_id=self.request.user.id)
        return ctx