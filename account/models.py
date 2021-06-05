from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager):
    # create_user deals with creating the user of costumer type
    def create_customer(self, email, name, contact_number, DOB,Target_competetive_exam,Current_education_status,Current_city,Home_City,Bio, Pic,viewpass=None,password=None, ):
        if not email:
            raise ValueError("enter email")
        if not name:
            raise ValueError("enter first name")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact_number=contact_number,
            Pic=Pic,
            DOB=DOB,
            Target_competetive_exam=Target_competetive_exam,
            Current_education_status=Current_education_status,
            Current_city=Current_city,
            Home_City=Home_City,
            Bio=Bio,

        viewpass=viewpass,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_vendor(self, shop_number, shop_name, shop_add, plan, gst, vendor, subscripton_amount):

        user = self.model(
            shop_number=shop_number,
            shop_name=shop_name,
            shop_add=shop_add,
            plan=plan,
            gst=gst,
            vendor=vendor,
            subscripton_amount=subscripton_amount,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, contact_number, password):
        user = self.create_customer(
            email=self.normalize_email(email),
            name=name,
            contact_number=contact_number,
            # viewpass=viewpass,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_uplaod_file_name(userpic, filename,):
    return u'shop/%s/%s%s' % (str(userpic.user_id),"",filename)
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    viewpass = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100)
    contact_number = models.IntegerField(null=True, blank=True, default=00000)
    address=models.CharField(max_length=30, null=True, blank=True)
    Pic=models.ImageField(upload_to=get_uplaod_file_name, default='/general/titlelogo.png', )
    DOB=models.DateTimeField(null=True, blank=True)
    Target_competetive_exam=models.CharField(max_length=30, null=True, blank=True)
    Current_education_status=models.CharField(max_length=30, null=True, blank=True)
    Current_city=models.CharField(max_length=30, null=True, blank=True)
    Home_City=models.CharField(max_length=30, null=True, blank=True)
    Bio=models.CharField(max_length=30, null=True, blank=True)
    Is_mentor=models.BooleanField(default=False)
    Is_teacher=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

def get_uplaod_file_name(userpic, filename,):
    return u'shop/%s/%s%s' % (str(userpic.vendor_id)+"/template","",filename)
def get_uplaod_file_name_blog(userpic, filename,):
    return u'blog/%s/%s%s' % (str(userpic.blogger_id)+"/template","",filename)

class VendorAccount(models.Model):
    vendor = models.OneToOneField(Account, default=None, on_delete=models.DO_NOTHING, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    shop_number = models.IntegerField(null=True, blank=True)
    plan = models.CharField(max_length=20, default="no active plan")
    template = models.CharField(max_length=20, default="default,default")
    subscripton_amount = models.IntegerField(null=True, blank=True)
    shop_name = models.CharField(max_length=150, unique=True)
    shop_add = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    gst = models.CharField(max_length=30 ,null=True, blank=True)
    logo = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/titlelogo.png', )
    corousel1 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/main-slider1.jpg')
    corousel2 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/main-slider2.jpg')
    corousel3 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/main-slider3.jpg')
    corousel4 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/slider1.jpg')
    corousel5 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/main-slider1.jpg')
    corousel6 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/slider1.jpg')
    corousel7 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/slider2.jpg')
    corousel8 = models.ImageField(upload_to=get_uplaod_file_name, default='/default-img/slider4.jpg')
    subscription_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # objects= MyAccountManager()
    def __str__(self):
        return self.shop_name

# only has permission to make changes or view anything in django administration can change it to staff later
#     def has_perm(self, perm,obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True
class BloggerAccount(models.Model):
    # Blogger_id = models.AutoField(primary_key=True)
    blogger = models.OneToOneField(Account, default=None, on_delete=models.DO_NOTHING, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    plan = models.CharField(max_length=20, default="no active plan")
    subscripton_amount = models.IntegerField(null=True, blank=True)
    blogname = models.CharField(max_length=30, unique=True)
    bio = models.CharField(max_length=150,null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    template = models.CharField(max_length=20, default="default,default")
    logo = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/titlelogo.png', )
    corousel1 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/main-slider1.jpg')
    corousel2 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/main-slider2.jpg')
    corousel3 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/main-slider3.jpg')
    corousel4 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/slider1.jpg')
    corousel5 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/main-slider1.jpg')
    corousel6 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/slider1.jpg')
    corousel7 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/slider2.jpg')
    corousel8 = models.ImageField(upload_to=get_uplaod_file_name_blog, default='/default-img/slider4.jpg')
    subscription_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email