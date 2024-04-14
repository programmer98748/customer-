from dashboard.models import *

def navbar_categories(request):
   
   # categories = Category.objects.all()

   # home = Pagehome.objects.all()


    information_site = InformaionSite.objects.all()
  
  #  name_website = InformaionSite.objects.get(pk=1)
    



    return {'information_site':information_site,}
