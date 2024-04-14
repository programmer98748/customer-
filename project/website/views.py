from django.shortcuts import render, redirect
from django.contrib import auth, messages

from dashboard.models import *
# Create your views here.
from .forms import *
def index(request):
    services = Services.objects.all()
    brands = Brands.objects.all()

    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f' لقد تم حفظ التعديل بنجاح')

            return redirect('website:index')
    else:
        form = ContactForm()
    context = {'services':services,'form':form,'Brands':brands}
    return render(request, 'website/index.html',context)

def project(request):
    return render(request, 'website/project.html')
