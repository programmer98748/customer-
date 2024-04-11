from django.shortcuts import render

# Create your views here.
import random
from django.shortcuts import reverse
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import now
from django.db.models import Q
from .models import *
#from post.forms import CommentForm
from .forms import CommentForm

class PostList(ListView):
    """ Home page """
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 10
   

#def blog(request): 
 #   return render(request, 'blog/blog.html')


    
class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'blog/blog_single.html'
    context_object_name = 'post'
    form_class = CommentForm
    
    def get(self, request, *args, **kwargs):
        """ 
        overwrite get function to incrase views_count by 1 

        """
        post = self.get_object()
        post.views_count += 1
        post.save()
        return super().get(request,*args, **kwargs)
    
            
    def get_queryset(self):
        # render posts that active = true and published_at before now
        return self.model.objects.filter( Q(active=True) & Q(published_at__lte=now()) )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # related posts 

        posts = self.get_queryset()

        related_posts = None

        # if related_posts none render 3 random posts
        if not related_posts:
            posts_list = list(posts)
            related_posts = random.sample(posts_list, min(len(posts_list), 3))

        context['related_posts'] = related_posts

        # comments
        comments = Comment.objects.filter( Q(post=post) & Q(active=True) )

        context['comments'] = comments

        context['comment_form'] = CommentForm

        return context
    
    
    def post(self, request, *args, **kwargs):
        self.obj = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
        
    def form_valid(self, form):
        form_2 = form.save(commit=False)
        form_2.user = self.request.user
        form_2.post = self.get_object()
        form_2.save()
        return super().form_valid(form)        
    
    def get_success_url(self):
        return reverse('post:blog',) #kwargs={'slug': self.get_object().slug}


def blog_single(request):
    return render(request, 'blog/blog_single.html')


