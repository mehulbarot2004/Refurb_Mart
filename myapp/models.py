from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator

# Create your models here.

list= [
    ('1', 'Available'),
    ('2', 'UnAvailable')
]



class registermodel(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    phone=models.BigIntegerField(null=True)

    def __str__(self):
        return self.name

class category(models.Model):
    catname=models.CharField(max_length=30)

    def __str__(self):
        return self.catname


class refurbishedproductmodel(models.Model):


    name=models.CharField(max_length=20)
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=True)
    price=models.IntegerField(null=True)
    image = models.ImageField(upload_to='photos', null=True,validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    description=models.TextField()
    status=models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

    def admin_photos(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
    admin_photos.allow_tags = True

class newproductmodel(models.Model):
    userid=models.ForeignKey(registermodel,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=20)
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=True)
    price=models.IntegerField(null=True)
    image = models.ImageField(upload_to='photos', null=True)
    description=models.TextField()
    status=models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name


    def admin_photos(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    admin_photos.allow_tags = True



class cart(models.Model):
    userid = models.ForeignKey(registermodel,on_delete=models.CASCADE)
    productid = models.ForeignKey(newproductmodel,on_delete=models.CASCADE,null=True)
    rproductid = models.ForeignKey(refurbishedproductmodel, on_delete=models.CASCADE,null=True)

    quantity = models.IntegerField()
    totalamount = models.FloatField()
    orderstatus = models.IntegerField() # 1 - item added , 0 - item removed/orderplace
    orderid = models.IntegerField() # default - 0 , will update orderid after user places the order



class ordermodel(models.Model):
    userid = models.ForeignKey(registermodel,on_delete=models.CASCADE)
    finaltotal = models.FloatField()
    phone = models.BigIntegerField()
    address = models.TextField()
    paymode = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True,)
    status = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=255,null=True, blank=True)




class contact_us(models.Model):
    name=models.CharField(max_length=20)
    userid = models.ForeignKey(registermodel, on_delete=models.CASCADE, null=True)

    email = models.EmailField()
    subject=models.CharField(max_length=20)
    message=models.TextField()




