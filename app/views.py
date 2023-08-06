from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from .models import *
import random
import uuid
from django.core.mail import send_mail
from datetime import date,datetime
import re
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic.list import ListView
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .process import html_to_pdf
from django.template.loader import render_to_string
from django.views.generic import View


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# from app import product

def index(request):
 brandDetails = Brand.objects.all()
 productCategoryDetails = ProductCategory.objects.all()
 data = {
  'brandDetails':brandDetails,
  'productCategoryDetails':productCategoryDetails
 }


def isContainSpace(uName,character):
    res = None
    for i in range(0, len(uName)):
        if uName[i] == character:
            res = i + 1
            break
    
    if res == None:
        pass
    else:
        return True
    
def isFirstThreeCharacterLetter(subUname):
    count = 0

    firstThreeCh = subUname[0:3]

    for i in firstThreeCh:
        if((i >= "A" and i <= "Z") or (i >= "a" and i <= "z")):
            count += 1
        else:
            break
    
    return count

def isStringContainsNumberOrNot(puserFirstName):
    flag = 1

    for i in puserFirstName:
        if((i >= "A" and i <= "Z") or (i >= "a" and i <= "z") or (i == " ")):
            flag = 0
        else:
            flag = 1
            break
    
    if(flag == 1):
        return True
    else:
        pass

def userNameValidation(uName):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_name == uName):
            error_message = "Username already taken!"
            break

    return error_message

def userEmailValidation(uEmail):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_email == uEmail):
            error_message = "Email ID already taken!"
            break

    return error_message

def userMobileValidation(uMobile):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_mobile == uMobile):
            error_message = "Mobileno already taken!"
            break

    return error_message

def userImageValidation(puserImage):
    error_message = None
    userImage = str(puserImage)

    if(not(userImage.lower().endswith(('.png','.jpg','.jpeg')))):
        error_message = "Choose only image!"

    return error_message
    

def login(request):
    return render(request,'login.html')


def validationLogin(username,password,username1,flag):
    error_message = None
    if(not username):
        error_message = "Please enter username!"
    elif username:
            if not password:
                error_message = "Please enter password!"
            elif(username != username1):
                error_message = "Invalid username or password!"
            elif not flag:
                error_message = "Invalid username or password!"

    return error_message


def validationForgotPassword(userEmail,myUserEmail):
    error_message = None
    if(not userEmail):
        error_message = "Please enter email!"
    elif userEmail:
        if(userEmail != myUserEmail):
            error_message = "Please enter valid email"
    
    return error_message

def validationChangePassword(userNewPassword,userNewSamePassword):
    error_message = None
    
    if(not userNewPassword):
        error_message = "Please enter new password.!"
    elif(userNewPassword):
        if(len(userNewPassword) < 6 or len(userNewPassword) > 15):
            error_message = "Your new password at least 6 character long and not greater than 15 character!"
        elif(userNewPassword != userNewSamePassword):
            error_message = "Your new password and new same password didn't match!"            
    
    return error_message

def validationChangePasswordDirectly(userCurPassword,userNewPassword,userNewSamePassword,flag):
    error_message = None
    if(not userCurPassword):
        error_message = "Please enter current password!"
    elif userCurPassword:
        if not flag:
            error_message = "Your current password is invalid.!"
        elif(not userNewPassword):
            error_message = "Please enter your new password!"
        elif userNewPassword:
            if(len(userNewPassword) < 6 or len(userNewPassword) > 15):
                error_message = "Your new password at least 6 character long and not greater than 15 character!"
            elif(userNewPassword != userNewSamePassword):
                error_message = "Your new password and new same password didn't match!"            
    
    return error_message



def loginAction(request):
    if 'user_name' in request.session:
        messages.error(request,'You are already logged in!')
        return redirect('home')
    elif 'admin' in request.session:
        messages.error(request,'You are already logged in!')
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username1')
            password = request.POST.get('password1')
            error_message = None
            flag = None
            is_admin = 0
            username1 = None
            c1 = User.objects.all()
            for item in c1:
                if(username == item.user_name):
                    username1 = item.user_name
                    is_admin = 0
                    flag = check_password(password,item.user_password)
                    if(item.is_admin == 1):
                        is_admin = 1
            value={
                'uname':username
            }
        
            error_message = validationLogin(username,password,username1,flag)

            if not error_message:
                if(is_admin == 1):
                    request.session['admin'] = username
                    messages.success(request,'Login successfully!')
                    return redirect('home')
                else:
                    request.session['user_name'] = username
                    messages.success(request,'Login successfully!')
                    return redirect('home')

            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }
                return render(request, 'login.html',data)

        return render(request, 'login.html')
    

def index(request):
 brandDetails = Brand.objects.all()
 productCategoryDetails = ProductCategory.objects.all()
 data = {
  'brandDetails':brandDetails,
  'productCategoryDetails':productCategoryDetails
 }

 if 'user_name' in request.session:
        current_user = request.session['user_name']
        data = {
            'current_user':current_user,
            'brandDetails':brandDetails,
            'productCategoryDetails':productCategoryDetails
        }
        return render(request,'home.html',data)
 elif 'admin' in request.session:
        current_user = request.session['admin']
        data = {
            'current_admin':current_user,
            'brandDetails':brandDetails,
            'productCategoryDetails':productCategoryDetails
        }
        return render(request,'home.html',data)

 return render(request,'home.html',data)

def validationUserProfile(puserName,puserEmail,puserMobile,puserFirstName,puserLastName,count):
    regxEmail = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    regxMobile = re.compile("(0|91)?[-\s]?[6-9][0-9]{9}")
    error_message = None
    mycharacter = " "

    if(not puserName):
        error_message = "Username is must!"
    elif(puserName):
        if (len(puserName) < 6 or len(puserName) > 15):
            error_message = "Username atleast 6 character long and maximum 15 character!"
        elif (isContainSpace(puserName,mycharacter)):
            error_message = "Username does not contain space!"
        elif (count < 3):
            error_message = "First three character of username must be in letter!"
        elif (not puserEmail):
            error_message = "Email is required!"
        elif puserEmail:
            if(not(re.fullmatch(regxEmail,puserEmail))):
                error_message = "Invalid email!"
            elif(not puserFirstName):
                pass
            elif puserFirstName:
                if(isStringContainsNumberOrNot(puserFirstName)):
                    error_message = "First name not contains number or special character!"
                elif(not puserMobile):
                    error_message = "Mobile no required!"
                elif(puserMobile):
                    if(len(puserMobile) > 10):
                        error_message = "Enter valid mobile no!"
                    elif(not(re.fullmatch(regxMobile,puserMobile))):
                        error_message = "Enter valid mobile"
                    elif(not puserLastName):
                        pass
                    elif(puserLastName):
                        if(isStringContainsNumberOrNot(puserLastName)):
                            error_message = "Last name not contains number or special character!"
    
    return error_message



def validation(userName,userPassword,userConfirmPassword,userEmail,userMobile,user,count,myCharacter):
    regxEmail = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    regxMobile = re.compile("(0|91)?[-\s]?[6-9][0-9]{9}")
    error_message = None
    if(not userName):
        error_message = "Username is required!"
    elif userName:
        isUserNameExistOrNot = user.isUserExists()
        if (len(userName) < 6 or len(userName) > 15):
            error_message = "Username atleast 6 character long and maximum 15 character!"
        elif (isContainSpace(userName,myCharacter)):
            error_message = "Username does not contain space!"
        elif (count < 3):
            error_message = "First three character of username must be in letter!"
        elif (isUserNameExistOrNot):
            error_message = "Username already taken.!"
        elif (not userEmail):
            error_message = "Email is required!"
        elif userEmail:
            isEmailExistOrNot = user.isEmailExists()
            if(isEmailExistOrNot):
                error_message = "Email already taken!"
            elif(not(re.fullmatch(regxEmail,userEmail))):
                error_message = "Invalid email!"
            elif (not userPassword):
                error_message = "Password is required.!"
            elif userPassword:
                if (len(userPassword) < 6 or len(userPassword) > 15):
                        error_message = "Password atleast 6 character long and maximum 15 character!"
                elif (userPassword != userConfirmPassword):
                        error_message = "Password and confirm password must be same!"
                elif(not userMobile):
                    error_message = "Mobile no is required!"
                elif userMobile:
                    isMobileExistOrNot = user.isMobileNoExists()
                    if(isMobileExistOrNot):
                        error_message = "Mobile no already taken!"
                    elif(len(userMobile) > 10):
                        error_message = "Enter valid mobile no!" 
                    elif(not(re.fullmatch(regxMobile,userMobile))):
                        error_message = "Enter valid mobile no"
    
    return error_message

def goSignUpPage(request):
    if 'user_name' in request.session:
        messages.error(request,'You are already registered!')
        return redirect('home')
        
    else: 
        if request.method == 'POST':
            postData = request.POST
            userName = postData.get('userName')
            userPassword = postData.get('userPassword')
            userConfirmPassword = postData.get('userConfirmPassword')
            userEmail = postData.get('userEmail')
            userMobile = postData.get('userMobileNo')
            userSecQue = postData.get('userSecQue')
            userSecAns = postData.get('userSecAns')
            salonData = Salon.objects.first()
            firstArea = Area.objects.first()
            myCharacter = " "

            count = isFirstThreeCharacterLetter(userName)

            #validation

            error_message = None

            value = {
                'uName':userName,
                'uEmail':userEmail,
                'uMobile':userMobile
            }

            user = User(user_name=userName,
                            user_password=userPassword,
                            user_email=userEmail,
                            user_mobile=userMobile,
                            user_sec_question=userSecQue,
                            user_sec_answer=userSecAns,
                            is_admin=0,
                            pincode=Area.objects.get(pincode=firstArea.pincode),
                            idsalon=Salon.objects.get(idsalon=salonData.idsalon),
                            )
        
            error_message = validation(userName,userPassword,userConfirmPassword,userEmail,userMobile,user,count,myCharacter)

            if not error_message: 
                user.user_password = make_password(user.user_password)
                user.register()
                request.session['user_name'] = userName
                messages.success(request,'Registration done successfully!')
                return redirect('home')
        
            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }
                return render(request, 'signup.html',data)

        return render(request, 'signup.html')

def logout(request):
    if 'user_name' in request.session:
        del request.session['user_name']
        messages.success(request,'Logout successfully!')
    else:
        messages.error(request,'You are not logged in!')
    return redirect('home')

def AdminLogout(request):
    if 'admin' in request.session:
        del request.session['admin']
        messages.success(request,'Logout successfully!')
    else:
        messages.error(request,'You are not logged in!')
    return redirect('home')


def user_profile1(request):
    if 'user_name' not in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        u1 = User.objects.filter(user_name=request.session['user_name'])
        u3 = User.objects.get(user_name=request.session['user_name'])
        data = {
            'user1':u1
        }

        if request.method == "POST":
            puserName = request.POST.get('update_username')
            puserEmail = request.POST.get('update_email')
            puserMobile = request.POST.get('update_mobile')
            puserFirstName = request.POST.get('update_First_Name')
            puserLastName = request.POST.get('update_Last_Name')
            error_message = None
            error_message1 = None
            success_message = None
            count = isFirstThreeCharacterLetter(puserName)

            error_message = validationUserProfile(puserName,puserEmail,puserMobile,puserFirstName,puserLastName,count)

            if not error_message:
                success_message = "Profile updated successfully!"

                for i in u1:
                    if(i.user_name != puserName):
                        error_message1 = userNameValidation(puserName)
                        break
                    elif(i.user_email != puserEmail):
                        error_message1 = userEmailValidation(puserEmail)
                        break
                    elif(i.user_mobile != puserMobile):
                        error_message1 = userMobileValidation(puserMobile)
                        break
                    elif(len(request.FILES) != 0):
                        puserImage = request.FILES['update_image']
                        error_message1 = userImageValidation(puserImage)
                        break

                if not error_message1:
                    u3.user_name = puserName
                    u3.user_email = puserEmail
                    u3.user_first_name = puserFirstName
                    u3.user_mobile = puserMobile
                    u3.user_last_name = puserLastName
                    if(len(request.FILES) != 0):
                        u3.user_image = request.FILES['update_image']
                
                    u3.save()
                    request.session['user_name'] = puserName
                    u1 = User.objects.filter(user_name = request.session['user_name'])
                    data = {
                        'user1':u1,
                        'success':success_message
                    }

                    return render(request,'user_profile.html',data)

                else:
                    data = {
                        'user1':u1,
                        'error1':error_message1
                    }
                    return render(request,'user_profile.html',data)
            else:
                data = {
                    'user1':u1,
                    'error':error_message
                }

                return render(request,'user_profile.html',data) 

        return render(request,'user_profile.html',data)

class ProductSubCategoryListView(ListView):
    model = ProductSubCategory
    template_name = 'productSubCategory.html'

    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        getCategory = ProductCategory.objects.get(id=int(self.kwargs['prodCatId']))
        if self.kwargs.get('prodCatId'):
            object_list = ProductSubCategory.objects.filter(pcategory=getCategory.id)
            if q:
                object_list = self.model.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)),pcategory=getCategory.id)
            else:
                object_list = ProductSubCategory.objects.filter(pcategory=getCategory.id)

        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productCategory"] = ProductCategory.objects.get(id=self.kwargs['prodCatId'])
        return context
    


class ProductListView(ListView):
    model = Product
    template_name = 'productPage.html'

    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        getCategory = ProductSubCategory.objects.get(id=int(self.kwargs['prodSubId']))
        if self.kwargs.get('prodSubId'):
            object_list = Product.objects.filter(psubcategory=getCategory.id)
            if q:
                object_list = self.model.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)),psubcategory=getCategory.id)
            else:
                object_list = Product.objects.filter(psubcategory=getCategory.id)

        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productCat"] = ProductCategory.objects.get(id=self.kwargs['prodCatId'])
        context["prodSubCat"] = ProductSubCategory.objects.get(id=self.kwargs['prodSubId'])

        return context

def productDetailsViewAllData(request,prodCatId,prodSubId,prodId):
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        u1 = User.objects.get(user_name=request.session['user_name'])
        i1 = Product.objects.get(id=prodId)
        productId = i1.id
        r1 = Review.objects.filter(product_idproduct=productId)
        try:
            r2 = Review.objects.get(product_idproduct=productId,user_iduser=u1.iduser)
        except:
            r2 = None
            print("error!")
        param = {'current_user':current_user,'itemName':i1,'currentUserDetails':u1,'usersReview':r1,'currentUserReview':r2}
        return render(request,'productDetailsPage.html',param)
    else:
        if 'admin' in request.session:
            admin = request.session['admin']  
        else:
            admin = None
        try:
            current_user = request.session['user_name']
            u1 = User.objects.get(user_name=request.session['user_name'])
        except:
            current_user = None
            u1 = None
        i1 = Product.objects.get(id=prodId)
        productId = i1.id
        r1 = Review.objects.filter(product_idproduct=productId)
        try:
            r2 = Review.objects.get(product_idproduct=productId,user_iduser=u1.iduser)
        except:
            r2 = None
            print("error!")
        param = {'current_user':current_user,'itemName':i1,'currentUserDetails':u1,'usersReview':r1,'currentUserReview':r2,'admin':admin}
        return render(request,'productDetailsPage.html',param)

def validationLogin(username,password,username1,flag):
    error_message = None
    if(not username):
        error_message = "Please enter username!"
    elif username:
            if not password:
                error_message = "Please enter password!"
            elif(username != username1):
                error_message = "Invalid username or password!"
            elif not flag:
                error_message = "Invalid username or password!"

    return error_message



def cartUser(request): 
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    cart1 = Cart.objects.filter(user=userId)
    data = {
        'userCart':cart1
    }
    if 'user_name' not in request.session:
        messages.error(request,'Login to continue!')
        return redirect('home')
    return render(request,'cart.html',data)

def addToCart(request):
  if request.method == "POST":
        if 'user_name' in request.session:
            u1 = User.objects.get(user_name=request.session['user_name'])
            prod_id = int(request.POST.get('prod_id'))
            ProductCheck = Product.objects.get(id=prod_id)
            if(ProductCheck):
                if(ProductCheck.offer_idoffer):
                    if(Cart.objects.filter(user=u1.iduser,product=prod_id)):
                        return JsonResponse({'data':"Product already in cart!"})
                    else:
                        prod_qty = int(request.POST.get('prod_qty'))
                        Cart.objects.create(user=User.objects.get(iduser=u1.iduser),product=Product.objects.get(id=prod_id),quantity=prod_qty,offer_record=0)
                        return JsonResponse({'status':"Product Added Successfully!"})
                elif(not ProductCheck.offer_idoffer):
                    if(Cart.objects.filter(user=u1.iduser,product=prod_id)):
                        return JsonResponse({'data':"Product already in cart!"})
                    else:
                        prod_qty = int(request.POST.get('prod_qty'))
                        Cart.objects.create(user=User.objects.get(iduser=u1.iduser),product=Product.objects.get(id=prod_id),quantity=prod_qty)
                        return JsonResponse({'status':"Product Added Successfully!"})
            else:
              return JsonResponse({'data':"No Such Product Found!"})
        else:
            return JsonResponse({'data':"Login to continue!"})
  return redirect('home')

def deleteCartProduct(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(Cart.objects.filter(user=userId, product=product_id)):
            cartitem = Cart.objects.get(product=product_id,user=userId)
            cartitem.delete()
        return JsonResponse({'status':"Product removed from cart!"})
    return redirect('home')

def updateUserCart(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(Cart.objects.filter(user=userId, product=product_id)):
            product_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product=product_id,user=userId)
            cart.quantity = product_qty
            cart.save()
            return JsonResponse({'status':"Cart updated successfully", 'error': 'errorrerer'})
    return redirect('home')


def checkoutProduct(request):
    u1 = User.objects.get(user_name=request.session['user_name'])
    c1 = City.objects.all()
    a1 = Area.objects.all()
    a2 = Area.objects.get(pincode=u1.pincode.pincode)
    delcharges = a2.area_delivery_charges
    userId = u1.iduser
    cartproducts = Cart.objects.filter(user=userId)
    cartOfferProduct = Cart.objects.filter(user=userId,offer_record=0)
    grand_total = 0
    total_offer_price = 0
    total_price = 0
    if(cartOfferProduct):
        for i in cartOfferProduct:
            total_offer_price = total_offer_price + i.product.offer_price * i.quantity
    else:
        total_offer_price = 0
    
    for item in cartproducts:
        total_price = total_price + (item.product.selling_price * item.quantity)

    grand_total = (total_price) - total_offer_price  
    context = {'cartproducts':cartproducts,'total_price':total_price, 'city':c1, 'area':a1,'current_user':u1,'delArea':delcharges,'offerPrice':total_offer_price,'grandTotal':grand_total}
    return render(request,'productcheckout.html',context)

def changecharges(request):
    if request.method == "POST":
        areaname = request.POST.get('areaname')
        a1 = Area.objects.get(area_name=areaname)
        return JsonResponse({'status':a1.area_delivery_charges})
    return redirect('home')


def placeorder(request):
    if request.method == "POST":
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        neworder = Order()
        neworder.user_iduser = User.objects.get(iduser=userId)
        neworder.orderfname = request.POST.get('fname')
        neworder.orderlname = request.POST.get('lname')
        neworder.orderemail = request.POST.get('email')
        neworder.ordermobile = request.POST.get('mobile')
        neworder.order_delivery_address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        a1 = Area.objects.get(area_name=request.POST['area1'])
        neworder.area_pincode = Area.objects.get(pincode=a1.pincode)
        neworder.order_payment_method = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        userpincode = request.POST.get('pincode')

        cart = Cart.objects.filter(user=userId)
        cartOfferProduct = Cart.objects.filter(user=userId,offer_record=0)
        total_offer_price = 0
        if(cartOfferProduct):
            for i in cartOfferProduct:
                total_offer_price = total_offer_price + i.product.offer_price * i.quantity
        else:
            total_offer_price = 0

        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + (item.product.selling_price * item.quantity)

        cart_total_price = (cart_total_price - total_offer_price)
        neworder.total_amount = cart_total_price + a1.area_delivery_charges

        trackno = 'variety'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'brewer'+str(random.randint(1111111,9999999))
        neworder.tracking_no = trackno

        currentDateTime2 = datetime.now()
        neworder.created_at = datetime(currentDateTime2.year,currentDateTime2.month,currentDateTime2.day,currentDateTime2.hour,currentDateTime2.minute,currentDateTime2.second)
        neworder.save()

        neworderitem = Cart.objects.filter(user=userId)
        for item in neworderitem:
            OrderedProduct.objects.create(
                order_idorder = neworder,
                product_idProduct = item.product,
                price = item.product.selling_price,
                quantity = item.quantity
            )

        Cart.objects.filter(user=userId).delete()
        u1.user_address = neworder.order_delivery_address
        u1.pincode = neworder.area_pincode
        u1.save()

        payMode = request.POST.get('payment_mode')
        if(payMode == "Paid by Razorpay" or payMode == "paid by paypal"):
            return JsonResponse({'status':"Your order has been placed successfully!"})
        else:
            messages.success(request,"Your order has been placed successfully!")
    
    return redirect('home')


def reviewsubmit(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if 'user_name' in request.session:
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        try:
            if(Review.objects.get(user_iduser=userId,product_idproduct=product_id)):
                r1 = Review.objects.get(user_iduser=userId,product_idproduct=product_id)
                ratingValue = request.POST.get('rating')
                if(not ratingValue):
                    r1.rating_value = 0
                else:
                    r1.rating_value = request.POST.get('rating')
                r1.subject = request.POST.get('subject')
                r1.review_description = request.POST.get('review')
                r1.reviewDate = date.today()
                r1.save()
                messages.success(request,'Review updated successfully!')
                return redirect(url)
        except:
            if request.method == "POST":
                userReview = Review()
                ratingValue = request.POST.get('rating')
                if(not ratingValue):
                    userReview.rating_value = 0
                else:
                    userReview.rating_value = request.POST.get('rating')
                userReview.subject = request.POST.get('subject')
                userReview.review_description = request.POST.get('review')

                userReview.user_iduser = User.objects.get(iduser=u1.iduser)
                userReview.product_idproduct = Product.objects.get(id=product_id)
                userReview.reviewDate = date.today()
                userReview.save()
                messages.success(request,'Review added successfully!')
            return redirect(url)
    else:
        messages.error(request,'Login to continue!')
        return redirect(url)

def signup(request):
    return render(request,'signup.html')

def forgot_password(request):
    return render(request,'forgot_password.html')

def directly_change_password(request):
    return render(request,'directly_change_password.html')

def user_profile(request):
    return render(request,'user_profile.html')




def change_password(request):
    return render(request,'change_password.html')


def error_404_view(request,exception):
    return render(request,'404.html')

def cart(request):
    return render(request,'cart.html')



def orderpage(request):
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    orders = Order.objects.filter(user_iduser=userId)
    context = {'userOrderData':orders}
    return render(request,'user_order.html',context)

def orderdetailspage(request,t_no):
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.id
    order = Order.objects.filter(tracking_no=t_no).filter(user_iduser=userId).first()
    orderitems = OrderedProduct.objects.filter(order_idorder=order)
    context = {'userOrderData':order,'userOrderDetails':orderitems}
    return render(request,'userOrderDetails.html',context)



class orderInvoicePdf(View):
    def get(self, request, *args, **kwargs):
        totalOfferPrice = 0
        totalPrice = 0
        current_user = request.session['user_name']
        cusername = User.objects.get(user_name=current_user)
        u1 = cusername.iduser
        o1 = Order.objects.get(tracking_no=self.kwargs['t_no'])

        od1 = OrderedProduct.objects.filter(order_idorder=o1.idorder)
        if od1:
            for i in od1:
                totalOfferPrice = totalOfferPrice + i.product_idProduct.offer_price
        else:
            totalOfferPrice=0

        for i in od1:
            totalPrice = totalPrice + i.product_idProduct.selling_price

        data = {
            'order':o1,
            'orderDetails':od1,
            'totalOfferPrice':totalOfferPrice,
            'totalPrice':totalPrice
        }
        open('app/templates/temp.html',"w").write(render_to_string("invoice.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')








class ProductSubCategoryListView(ListView):
    model = ProductSubCategory
    template_name = 'productSubCategory.html'

    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        getCategory = ProductCategory.objects.get(id=int(self.kwargs['prodCatId']))
        if self.kwargs.get('prodCatId'):
            object_list = ProductSubCategory.objects.filter(pcategory=getCategory.id)
            if q:
                object_list = self.model.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)),pcategory=getCategory.id)
            else:
                object_list = ProductSubCategory.objects.filter(pcategory=getCategory.id)

        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productCategory"] = ProductCategory.objects.get(id=self.kwargs['prodCatId'])
        return context
    

def orderCancel(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        userOrder = Order.objects.get(tracking_no=order_id)
        if(userOrder.order_payment_method == "COD"):
            userOrder.is_cancel_order = 1
            userOrder.cancel_order_date = datetime.now()
            orderedItemDelete = OrderedProduct.objects.get(order_idorder=userOrder.idorder)
            print(orderedItemDelete)
            orderedItemDelete.delete()
            userOrder.save()
            return JsonResponse({'status':"Order Cancel successfully!"})
    return redirect('home')

def offer(request):
    current_user = request.session['user_name']
    current_date = date.today()
    allItems = Product.objects.filter(offer_idoffer__isnull=False)
    for i in allItems:
        i.offer_price = (i.selling_price * int(i.offer_idoffer.offer_value)) / 100
        i.save()
        
        if(i.offer_idoffer.offer_end_date < date.today()):
            getOffer = Offer.objects.get(idoffer=i.offer_idoffer.idoffer)
            getOffer.delete()
    
    param = {'current_user':current_user,'allItem':allItems,'currentDate':current_date}
    return render(request,'offer.html',param)

class BrandListView(ListView):
    model = Brand
    template_name = 'brand.html'
    queryset = Brand.objects.all()

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            object_list = self.model.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        else:
            object_list = self.model.objects.all()
        return object_list

class BrandProductListView(ListView):
    model = Product
    template_name = 'brandproducts.html'


    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        getBrand = Brand.objects.get(id=int(self.kwargs['brand_id']))
        if self.kwargs.get('brand_id'):
            object_list = Product.objects.filter(brand=getBrand.id)
            if q:
                object_list = self.model.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)),brand=getBrand.id)
            else:
                object_list = Product.objects.filter(brand=getBrand.id)

        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.get(id=self.kwargs['brand_id'])
        return context

def BrandProductDetails(request,brand_id,product_id):
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        u1 = User.objects.get(user_name=request.session['user_name'])
        i1 = Product.objects.get(id=product_id)
        productId = i1.id
        r1 = Review.objects.filter(product_idproduct=productId)
        try:
            r2 = Review.objects.get(product_idproduct=productId,user_iduser=u1.iduser)
        except:
            r2 = None
            print("error!")
        param = {'current_user':current_user,'itemName':i1,'currentUserDetails':u1,'usersReview':r1,'currentUserReview':r2}
        return render(request,'productDetailsPage.html',param)
    else:
        if 'admin' in request.session:
            admin = request.session['admin']  
        else:
            admin = None
        try:
            current_user = request.session['user_name']
            u1 = User.objects.get(user_name=request.session['user_name'])
        except:
            current_user = None
            u1 = None
        i1 = Product.objects.get(id=product_id)
        productId = i1.id
        r1 = Review.objects.filter(product_idproduct=productId)
        try:
            r2 = Review.objects.get(product_idproduct=productId,user_iduser=u1.iduser)
        except:
            r2 = None
            print("error!")
        param = {'current_user':current_user,'itemName':i1,'currentUserDetails':u1,'usersReview':r1,'currentUserReview':r2,'admin':admin}
        return render(request,'productDetailsPage.html',param)

def forgot_password(request):
    if 'user_name' in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        if request.method == "POST":
            userEmail = request.POST.get('uEmail')
            myUserEmail = None
            error_message = None
            success_message = None
            token = str(uuid.uuid4())

            c1 = User.objects.all()

            for item in c1:
                if(item.user_email == userEmail):
                    myUserEmail = item.user_email
                    User.objects.filter(user_email = userEmail).update(forgot_password_token = token)
                    break
        
            value = {
                'email':userEmail
            }
            error_message = validationForgotPassword(userEmail,myUserEmail)

            if not error_message:
                success_message = "Your password reset link is sent to your email ID successfully!"
                subject = 'Welcome to variety shop!'
                myMessage = f'Hello user, your password reset link is http://127.0.0.1:8000/change_password/{token}/:, thank you for visiting our site!'
                email_from = 'purveshpc123@gmail.com'
                recipient_list = [myUserEmail,]
                data = {
                    'success' : success_message
                }
                send_mail(subject, myMessage, email_from, recipient_list)
                return render(request,'forgot_password.html',data)
        
            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }

                return render(request, 'forgot_password.html',data)


        return render(request,'forgot_password.html')

def change_password(request,token):
    if 'user_name' in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:  
        if request.method == "POST":
            userNewPassword = request.POST.get('userNewPassword')
            userSameNewPassword = request.POST.get('userSameNewPassword')
            error_message = None

            u1 = User.objects.get(forgot_password_token = token)

            error_message = validationChangePassword(userNewPassword,userSameNewPassword)

            if not error_message:
                u1.user_password = make_password(userNewPassword)
                u1.register()
                messages.success(request,'Password has been changed!')
                return redirect('home')
        
            else:
                data = {
                    'error' : error_message
                }

                return render(request,'change_password.html',data)

        return render(request,'change_password.html')

def directly_change_pass(request):
    if 'user_name' not in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        if request.method == "POST":
            userCurrentPassword = request.POST.get('userCurrentPassword')
            userNewPassword = request.POST.get('userNewPassword')
            userNewSamePassword = request.POST.get('userSameNewPassword')
            error_message = None
            flag = None

            current_user = request.session['user_name']

            u1 = User.objects.all()
            u2 = User.objects.get(user_name=current_user)

            for item in u1:
                if(item.user_name == current_user):
                    flag = check_password(userCurrentPassword,item.user_password)
                    break
        
            value = {
                'uCurPass':userCurrentPassword
            }

            error_message = validationChangePasswordDirectly(userCurrentPassword,userNewPassword,userNewSamePassword,flag)

            if not error_message:
                u2.user_password = make_password(userNewPassword)
                u2.register()
                messages.success(request,'Password has been changed!')
                return redirect('home')
        
            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }

                return render(request,'directly_change_password.html',data)


        return render(request,'directly_change_password.html')
    


def report(request):
    return render(request,'report.html')




def show_product(request):
  p=Product.objects.all()
  data={'products':p,   
      }
  return render(request,'productReport.html',data)

def pdf_report_create(request):
    products = Product.objects.all()
    context = {'products': products}


    template = get_template('productReport.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')



def show_product_category(request):
  pc=ProductCategory.objects.all()
  data={'products':pc,   
      }
  return render(request,'categoryReport.html',data)

def pdf_report_create_category(request):
    products =ProductCategory.objects.all()
    context = {'products': products}


    template = get_template('categoryReport.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')

  


  
def show_product_subcategory(request):
  p=ProductSubCategory.objects.all()
  data={'products':p,   
      }
  return render(request,'subCategoryReport.html',data)

def pdf_report_create_subcategory(request):
    products = ProductSubCategory.objects.all()
    context = {'products': products}


    template = get_template('subCategoryReport.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')


 
def show_product_brand(request):
  p=Brand.objects.all()
  data={'products':p,   
      }
  return render(request,'BrandReport.html',data)

def pdf_report_create_brand(request):
    products = Brand.objects.all()
    context = {'products': products}


    template = get_template('BrandReport.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')

 
def show_product_review(request):
  p=Review.objects.all()
  data={'products':p,   
      }
  return render(request,'reviewReport.html',data)

def pdf_report_create_review(request):
    products = Review.objects.all()
    context = {'products': products}


    template = get_template('reviewReport.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')



def show_order(request):
  p=OrderedProduct.objects.all()
  data={'products':p,   
      }
  return render(request,'orderReport.html',data)

def pdf_report_create_order(request):
    products = OrderedProduct.objects.all()
    context = {'products': products}


    template = get_template('orderReport.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')



def show_cart(request):
  p=Cart.objects.all()
  data={'products':p,   
      }
  return render(request,'cartReport.html',data)

def pdf_report_create_cart(request):
    products = Cart.objects.all()
    context = {'products': products}


    template = get_template('cartReport.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')


