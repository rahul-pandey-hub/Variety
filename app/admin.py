from django.contrib import admin

# Register your models here.
 

from .models import(
    City,
    Area,
    User,
    Salon,
    Brand,
    ProductCategory,
    ProductSubCategory,
    Offer,
    Product,
    Cart,
    Order,
    OrderedProduct,
    Review,
)

@admin.register(City)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ['idcity','city_name']
    list_per_page=5
    search_fields=('city_name',)

@admin.register(Area)
class AreaModelAdmin(admin.ModelAdmin):
    list_display = ['pincode','area_name','area_delivery_charges','city_idcity']
    list_per_page=5
    search_fields=('area_name',)
    

@admin.register(Salon)
class SalonModelAdmin(admin.ModelAdmin):
    list_display = ['idsalon','salon_name','salon_email','salon_phone','salon_description','salon_image','salon_address','area_pincode']

@admin.register(User)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['iduser','user_first_name','user_last_name','user_name','user_password','user_email','user_mobile','user_address','user_sec_question','user_sec_answer','user_image','is_admin','forgot_password_token','pincode','idsalon']
    list_per_page=5
    search_fields=('user_name','iduser',)
    
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
    list_per_page=5
    search_fields=('title',)
    list_filter=('title',)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
    list_per_page=5
    search_fields=('title',)
    list_filter=('title',)

@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','pcategory','psubimage']
    list_per_page=5
    search_fields=('title',)
    list_filter=('title',)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','psubcategory','brand','product_image','offer_idoffer']
    list_per_page=5
    search_fields=('title',)
    list_filter=('title',)

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity','created_at']
    list_per_page=5

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=['idorder','orderfname','orderlname','orderemail','ordermobile','order_date','cancel_order_date','order_delivery_date','order_delivery_address','city','total_amount','order_payment_method','payment_id','order_status','message','tracking_no','is_cancel_order','area_pincode','user_iduser','created_at']
    list_per_page=5

@admin.register(OrderedProduct)
class OrderProductModelAdmin(admin.ModelAdmin):
    list_display=['order_idorder','product_idProduct','price','quantity']
    list_per_page=5

@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display=['idreview','subject','review_description','rating_value','status','reviewDate','created_at','updated_at','user_iduser','product_idproduct']
    list_per_page=5
    list_filter=('product_idproduct',)

@admin.register(Offer)
class OfferModelAdmin(admin.ModelAdmin):
    list_display=['idoffer','offer_value','offer_start_date','offer_end_date','offer_description']
    list_per_page=5
    search_fields=('offer_value','offer_description',)