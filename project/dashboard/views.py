from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django import template
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import *
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from post.models import *
from .decorators import admin_and_editor_only, admin_only



from django.shortcuts import render, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

#@method_decorator(admin_and_editor_only, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard/post/post_list.html'
    context_object_name = 'posts'

#@method_decorator(admin_and_editor_only, name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'dashboard/post/post_form.html'
    form_class = PostForm
    post_slug = None

    def form_valid(self, form):
        form_2 = form.save(commit=False)
        form_2.author = self.request.user
        form_2.save()
        self.post_slug = form_2.slug
        messages.success(self.request, f'"{form.instance.title}" has been created successfully')
            
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('dashboard:post')


@user_passes_test(lambda u: u.is_superuser)
def post_update(request, id ):
    formm = Post.objects.get(id=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=formm)
        if form.is_valid():
            form.save()
            messages.success(request, f' لقد تم حفظ التعديل بنجاح')
            return HttpResponseRedirect('/dashboard/category')
    else:
        form = PostForm(instance=formm)
    context={
        'form':form,
    }
    return render(request, 'dashboard/post/post_form.html', context)
##

def post_delete(request, id):
    category = Post.objects.get(id=id)
    category.delete()
    messages.success(request, f"  تم الحذف بنجاح")
    return redirect(reverse('dashboard:posts'))



# Comments Views

@method_decorator(admin_and_editor_only, name='dispatch')
class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'dashboard/comment_list.html'
    context_object_name = 'comments'
 
def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    messages.success(request, f"  تم الحذف بنجاح")
    return redirect(reverse('dashboard:comments'))


#@method_decorator(admin_and_editor_only, name='dispatch')
class PostLanguageListView(LoginRequiredMixin, ListView):
    model = PostLanguage
    template_name = 'dashboard/post/posts_lang_lish.html'
    context_object_name = 'posts'

#@method_decorator(admin_and_editor_only, name='dispatch')
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:posts')     
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'"{self.get_object()}" has been deleted successfully')
        return super().delete(request, *args, **kwargs)

#@method_decorator(admin_and_editor_only, name='dispatch')
class PostLanguageCreateView(LoginRequiredMixin, CreateView):
    model = PostLanguage
    template_name = 'dashboard/post/post_form.html'
    form_class = PostLanguageForm
    success_url = reverse_lazy('dashboard:posts')
    post_slug = None

    def get_form(self):
        form = PostLanguageForm(initial={'post':self.kwargs.get('id'), 'language':'1'})
        
        if self.request.method == 'POST':
            form = PostLanguageForm(self.request.POST)
    
        return form

        
    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" has been created successfully')
        return super().form_valid(form)

#@method_decorator(admin_and_editor_only, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'dashboard/post_form.html'
    form_class = PostForm
    post_slug = None
    
    def test_func(self):
        return self.request.user.is_superuser or self.get_object().author == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" has been updated successfully')
        post = form.save()
        self.post_slug = post.slug
        return super().form_valid(form)    
    
        
    def get_success_url(self):
        return reverse('post:blog', kwargs={'slug':self.post_slug})    



#@method_decorator(admin_and_editor_only, name='dispatch')
class PostLanguageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostLanguage
    template_name = 'dashboard/post_form.html'
    form_class = PostLanguageForm
    post_slug = None
    
    def test_func(self):
        return self.request.user.is_superuser or self.get_object().post.author == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" has been updated successfully')
        post = form.save()
        self.post_slug = post.post.slug
        return super().form_valid(form)    
        
    def get_success_url(self):
        return reverse('post:post', kwargs={'slug':self.post_slug})    

#@method_decorator(admin_and_editor_only, name='dispatch')
class PostLanguageDeleteView(LoginRequiredMixin, DeleteView):
    model = PostLanguage
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:posts')     
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'"{self.get_object()}" has been deleted successfully')
        return super().delete(request, *args, **kwargs)



@user_passes_test(lambda u: u.is_superuser)
def post_language_update(request, pk ):
    formm = PostLanguage.objects.get(id=pk)
    if request.method == "POST":
        form = PostLanguageForm(request.POST, request.FILES, instance=formm)
        if form.is_valid():
            form.save()
            messages.success(request, f' لقد تم حفظ التعديل بنجاح')
            return HttpResponseRedirect('/dashboard/translation')
    else:
        form = PostLanguageForm(instance=formm)
    context={
        'form':form,
    }
    return render(request, 'dashboard/post/post_form.html', context)
##

def post_language_delete(request, pk):
    category = Post.objects.get(id=pk)
    category.delete()
    messages.success(request, f"  تم الحذف بنجاح")
    return redirect(reverse('dashboard:posts_language'))




#@method_decorator(admin_and_editor_only, name='dispatch')
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:posts')     
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'"{self.get_object()}" has been deleted successfully')
        return super().delete(request, *args, **kwargs)


####### brands ######
#@method_decorator(admin_and_editor_only, name='dispatch')
def brands(request):
    brands = Brands.objects.all()
    ##
    context = {'brands':brands}
    return render(request, 'dashboard/brands/brands.html', context)
####
#
def brands_add(request):
    if request.method == "POST":
        form = BrandsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f' لقد تم حفظ التعديل بنجاح')

            return HttpResponseRedirect('/dashboard/brands')
    else:
        form = BrandsForm()
    context={
        'form':form,

    }
    return render(request, 'dashboard/brands/brands_add.html', context)
#
def brands_delete(request, id):
    category = Brands.objects.get(id=id)
    category.delete()
    messages.success(request, f"  تم الحذف بنجاح")
    return redirect(reverse('dashboard:brands'))


    


def is_superuser(user):
    return user.is_superuser

### home ##
def index(request):
    services = Services.objects.all().count()
    post = Post.objects.all().count()
    if request.user.is_authenticated:
        user = request.user.username #.id
        context = {'services':services,'post':post}
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect('/dashboard/login')

####### category ######
#@method_decorator(admin_and_editor_only, name='dispatch')
def services(request):
    services = Services.objects.all()
    ##
    context = {'services':services}
    return render(request, 'dashboard/services/services.html', context)
####
#
def services_add(request):
    #formm = Category.objects.get(id=id)
    if request.method == "POST":
        form = ServicesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f' لقد تم حفظ التعديل بنجاح')

            return HttpResponseRedirect('/dashboard/services')
    else:
        form = ServicesForm()
    context={
        'form':form,

    }
    return render(request, 'dashboard/services/services_add.html', context)
#
@user_passes_test(lambda u: u.is_superuser)
def services_edite(request, id ):
    formm = Services.objects.get(id=id)
    if request.method == "POST":
        form = ServicesForm(request.POST, request.FILES, instance=formm)
        if form.is_valid():
            form.save()
            messages.success(request, f' لقد تم حفظ التعديل بنجاح')
            return HttpResponseRedirect('/dashboard/services')
    else:
        form = ServicesForm(instance=formm)
    context={
        'form':form,
    }
    return render(request, 'dashboard/services/services_edite.html', context)
##

def services_delete(request, id):
    service = Services.objects.get(id=id)
    service.delete()
    messages.success(request, f"  تم الحذف بنجاح")
    return redirect(reverse('dashboard:service'))


##### page ###
@user_passes_test(lambda u: u.is_superuser)
def page(request):
    post = Pages.objects.all()
    context = {'post':post,}
    return render(request, 'dashboard/page.html', context)

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Pages
    template_name = 'dashboard/page_add.html'
    form_class = PagesForm

    def form_valid(self, form):
        form_2 = form.save(commit=False)
        form_2.save()
        messages.success(self.request, f'"{form.instance.title}" has been created successfully')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('page')


@user_passes_test(lambda u: u.is_superuser)
def page_edite(request, id ):
    formm = Pages.objects.get(id=id)
    if request.method == "POST":
        form = PagesForm(request.POST, request.FILES, instance=formm)
        if form.is_valid():
            form.save()
            messages.success(request, f' لقد تم حفظ التعديل بنجاح')
            return HttpResponseRedirect('/dashboard/page')
    else:
        form = PagesForm(instance=formm)
    context={
        'form':form,
    }
    return render(request, 'dashboard/page_edite.html', context)

#
#def page_delete(request, id):
  #  product = Post.objects.get(id=id)
  #  product.delete()
 #   messages.success(request, f"  تم الحذف بنجاح")
  #  return redirect(reverse('dashboard:page'))

class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Pages
    template_name = 'dashboard/confirm_delete3.html'
    success_url = reverse_lazy('dashboard:page')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'"{self.get_object()}"  تم الحذف بنجاح')
        return super().delete(request, *args, **kwargs)

###### edite_informaion ###
@user_passes_test(lambda u: u.is_superuser)
def page_about(request):

    form_id = PageAbout.objects.first()
    if request.method == 'POST':
        form_infor = PageAboutForm(request.POST, instance=form_id)
        if form_infor.is_valid():
            form_infor.save()
            messages.success(request, f"تم التعديل  بنجاح")
    else:
        form_infor = PageAboutForm(instance=form_id)

    context = {
        'form':form_infor,}
    return render(request, 'dashboard/page_about.html', context)







######### gallery ####


@user_passes_test(lambda u: u.is_superuser)
def gallery(request):
    categories = Category.objects.all()

    selected_category = request.GET.get('category', None)
    images = Image.objects.all()  # Get all images initially

    if selected_category:
        images = Image.filter(category__name=selected_category)



    if request.method == 'POST':
        form= PhotosForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
            messages.success(request, f"تم الاضافة  بنجاح")
            return redirect(reverse('dashboard:gallery'))
    else:
        form = PhotosForm()
        print('hhhh')

    context = { 'images':images  ,'categories':categories,'form':form }
    return render(request, 'dashboard/gallery.html', context )

@user_passes_test(lambda u: u.is_superuser)
def delete(request):
    # Get the list of selected images
    selected_images = request.POST.getlist("images[]")

    # Delete the selected images
    if request.method == 'POST':

        for image_id in selected_images:
            image = Image.objects.get(id=image_id)
            #image.is_deleted = True
            image.delete()
        messages.success(request, f"تم الحذف بنجاح")


        return redirect(reverse('dashboard:gallery'))

from django.contrib.auth import logout

#### auth_logout ######
def auth_logout(request):
    logout(request)
    return redirect('dashboard:home')

##### profile #####
@user_passes_test(lambda u: u.is_superuser)
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='dashboard:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

###### edite_informaion ###
@user_passes_test(lambda u: u.is_superuser)
def edite_informaion(request):

    form_id = InformaionSite.objects.first()
    if request.method == 'POST':
        form_infor = InformaionSiteForm(request.POST,request.FILES, instance=form_id)
        if form_infor.is_valid():
            form_infor.save()
            messages.success(request, f"تم التعديل  بنجاح")
    else:
        form_infor = InformaionSiteForm(instance=form_id)



    context = {
        'form':form_infor,
    }

    return render(request, 'dashboard/edit_information.html', context)


## user ##
@method_decorator(user_passes_test(is_superuser), name="dispatch")
class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('dashboard:accounts')
    success_message = "Data successfully deleted"
##
@method_decorator(user_passes_test(is_superuser, login_url="/dashboard/"), name="dispatch")
class AEditUser(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('dashboard:accounts')
    success_message = "Data successfully updated"

##
@user_passes_test(lambda u: u.is_superuser)
def user_show(request):
    users = User.objects.all()
    if request.method == "POST":
        active = request.POST.get('active')
        if active == '1':
            active = True
        else:
            active = False
        user_id= title = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.is_staff =  active
        user.is_active = active
        user.is_superuser = active
        user.save()
    context = { 'users': users }
    return render(request, 'dashboard/list_users.html', context)

####
@method_decorator(user_passes_test(is_superuser, login_url="/dashboard/"), name="dispatch")
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

####
@method_decorator(user_passes_test(is_superuser, login_url="/dashboard/"), name="dispatch")
class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    msg = None
    success = False
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'نجحت إضافة المستخدم')
            success = True
            return redirect("/dashboard/accounts")
    else:
        form = CreateUserForm()
    return render(request, "dashboard/add_user.html", {"form": form, "msg": msg, "success": success})



@method_decorator(admin_only, name='dispatch')
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'dashboard/add_user.html'
    context_object_name = 'accounts'
    form_class = UserForm    
    success_url = reverse_lazy("dashboard:accounts")
    

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(self.request, f'"{form.instance.username}" has been created successfully')

        return super().form_valid(form)

@method_decorator(admin_only, name='dispatch')
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'dashboard/edit_user.html'
    context_object_name = 'account'
    form_class = UserUpdateForm    
    success_url = reverse_lazy("dashboard:accounts")    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['p_form'] = UpdateProfileForm(instance=self.get_object())
            
        return context
    
    def post(self, request, *args, **kwargs):
        form_2 = UpdateProfileForm(request.POST, request.FILES, instance=self.get_object())
        
        if form_2.is_valid():
            form_2.save()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        if form.is_valid():
            form.check_email(self.get_object().email)
            messages.success(self.request, f'"{form.instance.username}" has been updated successfully')
        return super().form_valid(form)    

@method_decorator(admin_only, name='dispatch')    
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'dashboard/confirm_delete3.html'
    success_url = reverse_lazy("dashboard:accounts")        
    
  

