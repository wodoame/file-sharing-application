from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User

class Index(View):
    def get(self, request):
        context = {'users':User.objects.all()}
        return render(request,'index.html', context)
  