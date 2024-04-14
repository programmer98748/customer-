import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.utils.translation import get_language
from PIL import Image
#from unidecode import unidecode
from django.utils.text import slugify

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("?", "")
    return str

def upload_image(instance, image_name):
    """ Make a path to the post image and change the name of the image to a post id

    Returns:
        [str]: [image path]
    """
    _ , extension = os.path.splitext(image_name)

    # return f"post_images/{instance.id}.{extension}"   
    return f"post_images/{instance.title}.{extension}"   

active_field_choices = [
    (True, _('Active')),
    (False, _('Inactive'))
]

class Language(models.Model):
    name = models.CharField(_('name'), max_length=25, null=True, blank=True)
    code = models.CharField(_('code'), max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=True)
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)

    def __str__(self):
        return self.code



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))
    title = models.CharField(_('title'), max_length=100)
    content = models.TextField(_('content'), max_length=4000)
    image = models.ImageField(_('image'), upload_to=upload_image, blank=False, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=True)
    published_at = models.DateTimeField(_('published at'), default=now)
    views_count = models.IntegerField(_('views count'), null=True, blank=True, default=0, editable=False)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='posts', verbose_name=_('language'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=100, allow_unicode=True)
    
    class Meta:
        ordering = ('-published_at', )
    
    @property
    def get_self_or_post_lang(self):
        # check are language existin Language model
        try:
            lang = Language.objects.get(code=get_language())
        except Language.DoesNotExist: # if not retrun default title
            return self
                    
        if self.language == lang:
            return self
        
        post_lang = self.post_lang.filter(language = lang)
        
        if post_lang:
            return post_lang.get()
        
        return self
        
    def get_title(self):
        return self.get_self_or_post_lang.title
    
    def get_content(self):
        return self.get_self_or_post_lang.content
    
   
    def get_language_code(self):
        return self.get_self_or_post_lang.language.code
            
        
    
    def __str__(self):
        return self.title
 
   
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        # Make a post Slug
  #      if not self.pk:
 #           slug = slugify(unidecode(f"{self.title}"))
#
   #         slug_count = len(Post.objects.filter(slug=slug))
  #          if slug_count > 0:
 #               slug = f"{slug}-{slug_count}"
#
           # self.slug = slug
    #       

        # Handle problem in upload_image function  (pk not generator yet)
        # if self.pk is None:
        #     post_image = self.image
        #     self.image = None
        #     super().save(*args, **kwargs)
        #     self.image = post_image

        super().save(*args, **kwargs)
        
        # image resize
        if self.image:
            try:
                img = Image.open(self.image.path)   
                if img.width > 800 or img.height > 800:
                    img.thumbnail( (800, 800) )
                    img.save(self.image.path)
            except:
                pass

class PostLanguage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_lang', verbose_name=_('post'))
    title = models.CharField(_('title'), max_length=100)
    content = models.TextField(_('content'), max_length=4000)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='posts_lan', verbose_name=_('language'))
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user_comment  = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField(_('content'), max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments', verbose_name=_('post'),)
    created_at = models.DateTimeField(_('created at'), auto_now=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=True)
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)
    
    def __str__(self):
        return self.content