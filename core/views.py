from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import UpdateProfileForm
from django.contrib.auth.decorators import login_required

class Index(View):
    def get(self, request):
        context = {'users':User.objects.all()}
        return render(request,'index.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})