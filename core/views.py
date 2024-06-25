from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import UploadFileForm
from .models import File, Folder
from .utils import SVGS, getExtension
from .components import renderFiles

class Index(View):
    def get(self, request):
        context = {'users':User.objects.all()}
        return render(request,'index.html', context)

# show all files
class Files(View):
    def get(self, request):
        context = {'files': ['lab-report.pdf','testimonial.pdf', 'school fees.pdf','random.pdf','attendance.xlsx','budget.xlsx']}
        return render(request, 'files.html', context) 

class UploadFile(View):
    def get(self, request):
        context = {}
        return render(request, 'upload-file.html', context)
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid(): 
            rootFolder, created = Folder.objects.get_or_create(
            name=f'{request.user.username}-root-folder',
            user=request.user)
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
    def get(self, request): 
        context = {}
        return render(request, 'files.html', context)

class RenderFiles(View):
    def get(self, request):
        html = renderFiles(request)
        return HttpResponse(html)
    
    