from django.urls import path, re_path
from django.views.static import serve
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app.views import orderInvoicePdf


urlpatterns = [
    path('', views.index,name="home"),
    path('add-to-cart',views.addToCart,name='add-to-cart'),
    path('signup',views.goSignUpPage,name='signup'),
    path('login',views.loginAction,name='login'),
    path('forgot_password',views.forgot_password,name='fpassword'),
    path('change_password/<token>/',views.change_password,name='change_password'),
    path('directly_change_password/',views.directly_change_pass,name='directlychangepass'),
    path('allBrands/',views.BrandListView.as_view(),name='brands'),
    path('currentBrandProducts/<int:brand_id>/',views.BrandProductListView.as_view(),name='currentBrandProducts'),
    path('currentBrandProducts/<int:brand_id>/<int:product_id>/',views.BrandProductDetails,name='currentBrandProductsDetails'),
    path('user_profile/',views.user_profile1,name='userProfile'),
    path('logout/',views.logout, name='logout'),
    path('userCart/',views.cartUser,name='userCurrentCart'),
    path('delete-cart-product',views.deleteCartProduct,name='delete-cart-product'),
    path('update-cart',views.updateUserCart,name='update-cart'),
    path('checkout/',views.checkoutProduct,name='checkout'),
    path('change-charges',views.changecharges,name='change-charges'),
    path('place-order',views.placeorder,name='place-order'),
    path('submit_review/<int:product_id>',views.reviewsubmit,name='submit_review'),
    path('offer',views.offer,name='offer'),

    path('productCategory/<int:prodCatId>/',views.ProductSubCategoryListView.as_view(),name='productCat'),
    path('productCategory/<int:prodCatId>/<int:prodSubId>/',views.ProductListView.as_view(),name='productOfSubCat'),
    path('productCategory/<int:prodCatId>/<int:prodSubId>/<int:prodId>/',views.productDetailsViewAllData,name='productDetailsViewPage'),
    
    path('my-orders',views.orderpage,name='my-orders'),
    path('orderview/<str:t_no>/',views.orderdetailspage,name='orderview'),
    path('cancelOrder',views.orderCancel,name='cancelOrder'),


    path('orderInvoice/<str:t_no>/',orderInvoicePdf.as_view(),name='orderInvoice'),


    path('report/',views.report,name='report'),
    
    path('show_products_report/',views.pdf_report_create,name='show_products_report'),
    path('show_products/',views.show_product,name='show_products'),

    path('pdf_report_create_category/',views.pdf_report_create_category,name='pdf_report_create_category'),
    path('show_product_category/',views.show_product_category,name='show_product_category'),

    path('pdf_report_create_subcategory/',views.pdf_report_create_subcategory,name='pdf_report_create_subcategory'),
    path('show_product_subcategory/',views.show_product_subcategory,name='show_product_subcategory'),

    path('pdf_report_create_brand/',views.pdf_report_create_brand,name='pdf_report_create_brand'),
    path('show_product_brand/',views.show_product_brand,name='show_product_brand'),

    path('pdf_report_create_review/',views.pdf_report_create_review,name='pdf_report_create_review'),
    path('show_product_review/',views.show_product_review,name='show_product_review'),

    path('pdf_report_create_order/',views.pdf_report_create_order,name='pdf_report_create_order'),
    path('show_order/',views.show_order,name='show_order'),

    path('pdf_report_create_cart/',views.pdf_report_create_cart,name='pdf_report_create_cart'),
    path('show_cart/',views.show_cart,name='show_cart'),






  
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



       



