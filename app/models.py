# Create your models here.

from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator
# from ckeditor.fields import RichTextField
import datetime
# from unittest.util import _MAX_LENGTH

STATE_CHOICE=(
    ('Andaman & Nicobar Island','Andaman & Nicobar Island'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Panjab','Panjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)

class City(models.Model):
    idcity = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'city'
    
    def __str__(self):
        return self.city_name


class Area(models.Model):
    pincode = models.DecimalField(primary_key=True,max_digits=6, decimal_places=0)
    area_name = models.CharField(max_length=100)
    area_delivery_charges = models.IntegerField()
    city_idcity = models.ForeignKey(City,on_delete=models.SET_NULL,null=True, db_column='city_idcity')

    class Meta:
        managed = True
        db_table = 'area'
    
    def __str__(self):
        return self.area_name
    

class Salon(models.Model):
    idsalon = models.AutoField(primary_key=True)
    salon_name = models.CharField(max_length=45)
    salon_email = models.CharField(max_length=45)
    salon_phone = models.DecimalField(max_digits=10, decimal_places=0,null=True)
    salon_description = models.CharField(max_length=200)
    salon_image = models.ImageField(upload_to='images',null=True,blank=True)
    salon_address = models.CharField(max_length=500,null=True)
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True, db_column='area_pincode')

    class Meta:
        managed = True
        db_table = 'salon'
    
    def __str__(self):
        return self.salon_name

class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    user_first_name = models.CharField(max_length=25,null=True)
    user_last_name = models.CharField(max_length=25,null=True)
    user_name = models.CharField(max_length=15,unique=True)
    user_password = models.CharField(max_length=300)
    user_email = models.CharField(max_length=245,unique=True)
    user_mobile = models.CharField(max_length=10,unique=True)
    user_address = models.TextField(max_length=200,null=True)
    user_sec_question = models.CharField(max_length=60,null=True)
    user_sec_answer = models.CharField(max_length=60,null=True)
    user_image = models.ImageField(upload_to='userimages',null=True,blank=True)
    is_admin = models.IntegerField(default=0)
    forgot_password_token = models.CharField(max_length=100,default="")
    pincode = models.ForeignKey(Area,null=True,on_delete=models.SET_NULL, db_column='area_pincode')
    idsalon = models.ForeignKey(Salon,null=True,on_delete=models.SET_NULL)

    class Meta:
        managed = True
        db_table = 'user'
    
    def __str__(self):
        return self.user_name

    def register(self):
        self.save()

    def isEmailExists(self):
        if User.objects.filter(user_email=self.user_email):
            return True
        return False

    def isUserExists(self):
        if User.objects.filter(user_name=self.user_name):
            return True
        return False

    def isMobileNoExists(self):
        if User.objects.filter(user_mobile=self.user_mobile):
            return True
        return False
    
    @staticmethod
    def get_user_by_username(user_name):
        return User.objects.get(user_name=user_name)

class Brand(models.Model):
    title = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class ProductCategory(models.Model):
    title = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    

class ProductSubCategory(models.Model):
    title = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=200)
    pcategory = models.ForeignKey(ProductCategory,on_delete=models.SET_NULL,null=True)
    psubimage = models.ImageField(upload_to="psubcatImage")

    def __str__(self):
        return self.title

class Offer(models.Model):
    idoffer = models.AutoField(primary_key=True)
    offer_value = models.DecimalField(max_digits=2, decimal_places=0)
    offer_start_date = models.DateField()
    offer_end_date = models.DateField()
    offer_description = models.CharField(max_length=200,)

    class Meta:
        managed = True
        db_table = 'offer'
    
    def __str__(self):
        return self.offer_description

class Product(models.Model):
    title = models.CharField(max_length=200,unique=True)
    selling_price = models. FloatField()
    discounted_price = models.FloatField()
    description=models.TextField()
    psubcategory = models.ForeignKey(ProductSubCategory,on_delete=models.SET_NULL,null=True)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    offer_price = models.FloatField(default=0)
    product_image=models.ImageField(upload_to='productimg')
    offer_idoffer=models.ForeignKey(Offer,on_delete=models.SET_NULL,null=True,blank=True)
 
    def __str__(self):
        return self.title
    


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=True)
    offer_record = models.IntegerField(default=1,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
 
    def __str__(self):
     return str(self.user)
    
    @property
    def total_cost(self):
        return self.quantity *self.product.discounted_price
 
    
    
class Order(models.Model):
    idorder = models.AutoField(primary_key=True)
    orderfname = models.CharField(max_length=150,null=True)
    orderlname = models.CharField(max_length=150,null=True)
    orderemail = models.CharField(max_length=150,null=True)
    ordermobile = models.CharField(max_length=150,null=True)
    order_date = models.DateField(auto_now_add=True)
    cancel_order_date = models.DateTimeField(blank=True,null=True)
    order_delivery_date = models.DateTimeField(auto_now_add=True)
    order_delivery_address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    total_amount = models.FloatField(null=False)
    order_payment_method = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=250,blank=True,null=True)
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered')
    )
    order_status = models.CharField(max_length=150,choices=STATUS_CHOICES,default='Pending')
    message = models.TextField(blank=True,null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    is_cancel_order = models.IntegerField(default=0)
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True, db_column='area_pincode')
    user_iduser = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, db_column='user_iduser')
    created_at = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'order'
    
    def __str__(self):
        return '{} - {}'.format(self.idorder,self.tracking_no)

class OrderedProduct(models.Model):
    order_idorder = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    product_idProduct = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'ordered_product'


class Review(models.Model):
    idreview = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100,blank=True)
    review_description = models.TextField(max_length=500,blank=True)
    rating_value = models.FloatField(null=True)
    status = models.BooleanField(default=True)
    reviewDate = models.DateField(datetime.date.today,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_iduser = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product_idproduct = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)

    class Meta:
        managed = True
        db_table = 'review'
