from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class NormalManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        result = super().get_queryset(*args,**kwargs).filter(role=User.Role.NORMAL)
        return result
class CompanyManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        result = super().get_queryset(*args,**kwargs).filter(role = User.Role.COMPANY)
        return result
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        NORMAL = "NORMAL", 'Normal'
        COMPANY = "COMPANY", 'Company'
        
    # base_role = Role.ADMIN
    
    phone = models.CharField(max_length=50,null=True,blank=True)
    
    role = models.CharField(max_length=50, choices=Role.choices,default = Role.ADMIN)
    
    company = CompanyManager()
    
    normal = NormalManager()
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ADMIN" or 'Admin':
        Profile.objects.bulk_create(
            [Profile(user=instance,meta_key="name"),
             Profile(user=instance,meta_key="IsAdmin",meta_value="true")]
            ) 
    elif created and instance.role == "NORMAL" or 'Normal':
        Profile.objects.bulk_create(
            [Profile(user=instance,meta_key="name"),
             Profile(user=instance,meta_key="wallet",meta_value=0),
             Profile(user=instance,meta_key="carbonProduce",meta_value=0.0000)]
            ) 
    elif created and instance.role == "COMPANY" or 'Company':
        Profile.objects.bulk_create(
            [Profile(user=instance,meta_key="companyName"),
             Profile(user=instance,meta_key="address"),
             Profile(user=instance,meta_key="vatNumber"),
             Profile(user=instance,meta_key="chairman")]
            )
 

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    meta_key = models.CharField(max_length=50)
    meta_value = models.CharField(max_length=255,null=True,blank=True)
