from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import UploadFileForm, CreateFolderForm
from .models import File, Folder
from .utils import SVGS, getExtension
from .components import renderFiles

class Index(View):
    def get(self, request):
        context = {'users':User.objects.all(), 'page':'home'}
        return render(request,'index.html', context)

# show all files
class Test(View):
    def get(self, request):
        context = {}
        return render(request, 'test.html', context) 

class UploadFile(View):
    def get(self, request):
        context = {'page': 'upload-file'}
        return render(request, 'upload-file.html', context)
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid(): 
            rootFolder, created = Folder.objects.get_or_create(name=f'{request.user.username}-root-folder')
            file: InMemoryUploadedFile = request.FILES.get('file')
            instance: File = form.save(commit=False)
            instance.name = file.name
            instance.folder = rootFolder
            instance.extension = getExtension(file.name)
            form.save()
        else:
            print(form.errors.as_data())

        return redirect('my-files')
    
    # * An uploaded file can be handled by some method
    def handleUploadedFile(self, f):
       pass

class MyFiles(View):
    template = 'files.html'
    
    def get(self, request): 
        context = {'page': 'my-files'}
        return render(request, 'files.html', context)
    
    def post(self, request):
        print(request.POST)
        form = CreateFolderForm(request.POST)
        if form.is_valid(): 
            instance = form.save(commit=False)
            instance.user = request.user
            instance.folder = Folder.objects.get(name=f'{request.user.username}-root-folder') # ! hard coded parent directory
            form.save() 
        else: 
            print(form.errors.as_data())
        return self.get(request)


class RenderFiles(View):
    def get(self, request):
        html = renderFiles(request)
        return HttpResponse(html)

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import forms

class TestLogin(View):
    template = 'login.html'
    
    def get(self, request):
        return render(request, self.template)
    
    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        print(request.POST)
        context = {} 
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else: 
            username = request.POST.get('username')
            context = {'invalidCredentials': True, 'username': username}
            print(form.errors.as_data())
        return render(request, self.template, context)
    
    