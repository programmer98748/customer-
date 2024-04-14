from django.db import models
from dashboard.models import Services
# Create your models here.

class ContactUs(models.Model):
    full_name = models.CharField(max_length=50)
    mobile  = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)

    subject = models.ForeignKey(
        Services,
        related_name='service_subject',
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = ("Info")
        verbose_name_plural = ("Infos")

    def __str__(self):
        return self.email
