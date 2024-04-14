from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language



from .decorators import get_or_create_editor_admin_group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_images')
   
    @property    
    def is_admin(self):        
        _ , admin_group = get_or_create_editor_admin_group()
        
        if self.user.is_superuser:
            return True

        elif self.user.groups.exists():
            if admin_group in self.user.groups.all():
                return True

        return False
    
    @property    
    def is_admin_or_editor(self):        
        editors_group , admin_group = get_or_create_editor_admin_group()
        
        if self.user.is_superuser:
            return True

        elif self.user.groups.exists():
            groups = self.user.groups.all()
            if admin_group in groups or editors_group in groups:
                return True

        return False
        
    def __str__(self):
        try:
            return self.user.username
        except:
     
            return "none"
            
    
    
    def save(self, *args, **kwargs):
        """
            Overwrite save mehtod to rename a image and resize a big image
        """
        
        # Handle problem in upload_image function  (pk not generator yet)
        if self.pk is None:
            image = self.picture
            self.picture = None
            super().save(*args, **kwargs)
            self.picture = image

        super().save(*args, **kwargs)
        
        # image resize
        img = Image.open(self.picture.path)   
        if img.width > 400 or img.height > 400:
            img.thumbnail( (400, 400) )
            img.save(self.picture.path)
            
        
    def __str__(self):
        return self.user.username
##
def image_upload(instance,filename):
    imagename , extension = filename.split(".")
    return "category/images/%s.%s"%(instance.id,extension)
##
class InformaionSite(models.Model):
    name_ar = models.CharField(_('name arabic'),max_length=60 , default='name')
    name_en = models.CharField(_('name english'),max_length=60 , default='name')

    description_ar = models.TextField(_('description arabic'),null=True, blank=True)
    description_en = models.TextField(_('description english'),null=True, blank=True)

    logo_white = models.ImageField(_('logo white'),upload_to='logo/', null=True, blank=True)
    logo_black = models.ImageField(_('logo icon black'),upload_to='logo/', null=True, blank=True)
    background_image = models.ImageField(_('background image'),upload_to='logo/', null=True, blank=True)
   
   # title_name =  models.CharField(_('title_name'),max_length=150)
    address = models.CharField(_('address'),max_length=60)
    email = models.EmailField(_('email'),null=True, blank=True)
    mobile = models.IntegerField(_('telephone'),null=True, blank=True)
    facebook = models.URLField(_('facebook'),null=True, blank=True)
    twitter = models.URLField(_('twitter'),null=True, blank=True)
    instagram = models.URLField(_('instagram'),null=True, blank=True)
    whatsapp = models.URLField(_('whatsapp'),null=True, blank=True)
    maps = models.CharField(_('maps'),max_length=200, null=True, blank=True)
    pubilished_at = models.DateTimeField(_('pubilished_at'),auto_now=True)

#    count_custemor = models.IntegerField(_('count_custemor'),)



##

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("?", "")
    return str
##
'''

class Post(models.Model):
    user = models.ForeignKey(User, related_name='user_blogs', on_delete=models.CASCADE)
    title  = models.CharField(max_length=60 ,blank=True, null=True)
    image = models.ImageField(upload_to='post/', null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    create_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=60,unique=True, allow_unicode=True, blank=True, null=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
'''

##
class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)

    image = models.ImageField(upload_to='category/', null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    create_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=60,unique=True, allow_unicode=True, blank=True, null=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = arabic_slugify(self.name)
        super(Category, self).save(*args, **kwargs)



    def __str__(self):
        return self.name
##
class Project(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=60 ,blank=False, null=True)
    image = models.ImageField(upload_to='category/', null=False, blank=False)
    location  = models.CharField(max_length=60 ,blank=True, null=True)
    description = models.TextField(null=True, blank=False)
    create_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=60,unique=True, allow_unicode=True, blank=True, null=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = arabic_slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
##
class Image(models.Model):
    image = models.ImageField(_('image'),upload_to=image_upload)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='project')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category
    @property

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
##
class Pages(models.Model):
    title  = models.CharField(max_length=60, blank=False)
    image = models.ImageField(upload_to='home/', null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PageAbout(models.Model):
    title_head  = models.CharField(max_length=60, null=False, blank=False)
    title_goal  = models.CharField(max_length=60, null=False, blank=False)
    description = models.TextField(null=True, blank=False)

   # image = models.ImageField(upload_to='services/', null=False, blank=False)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_head









from post.models import Language


active_field_choices = [
    (True, _('Active')),
    (False, _('Inactive'))
]

##
class Services(models.Model):
    title  = models.CharField(max_length=60, null=False, blank=False)
    image = models.ImageField(upload_to='services/', null=False, blank=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='services', verbose_name=_('language'), null=True, blank=True)

    url = models.URLField(null=False, blank=True)
    description = models.TextField(null=True, blank=False)
    create_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


    @property
    def get_self_or_services_lang(self):
        # check are language existin Language model
        try:
            lang = Language.objects.get(code=get_language())
        except Language.DoesNotExist: # if not retrun default title
            return self
                    
        if self.language == lang:
            return self
        
        services_lang = self.services_lang.filter(language = lang)
        
        if services_lang:
            return services_lang.get()
        
        return self

    def get_titles(self):
        return self.get_self_or_services_lang.title
    
    def get_descriptions(self):
        return self.get_self_or_services_lang.description
    
   # def get_categories(self):
   #     return self.get_self_or_services_lang.categories
    
    def get_language_codes(self):
        return self.get_self_or_services_lang.language.code
              
##
class TranslateTittle(models.Model):
    services = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='services_lang', verbose_name=_('services'))
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), max_length=4000)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='services_lan', verbose_name=_('language'))
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)

    def __str__(self):
        return self.title
 





##
class Brands(models.Model):
    image = models.ImageField(upload_to='Brands/', null=False, blank=True)
    url = models.URLField(null=False, blank=True)
    create_at = models.DateTimeField(auto_now=True)


   
