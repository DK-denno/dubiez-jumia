from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login,authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,EmailMultiAlternatives
from .models import Profile,Item,Cart,Seller,Messages,newsLetter,Address,Order
import datetime as dt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import signUpForm,profileForm,changePasswordForm,chatForm,addressForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    date = dt.date.today()
    items = Item.objects.all()
    return render(request, 'index.html',{"date":date, "items":items})


def signup(request):
    signup = signUpForm()
    if request.method == 'POST':
        signup = signUpForm(request.POST)
        if signup.is_valid():
            signup.save()
            username = signup.cleaned_data.get('username')
            email = signup.cleaned_data.get('email')
            raw_password = signup.cleaned_data.get('password1')
            user = authenticate(username=username,email=email, password=raw_password)
            profile = Profile(user=user)
            profile.save()
            user.is_active = True
            current_site = get_current_site(request)
            mail_subject = "Welcome to Our Online Shop"
            message = render_to_string('email/sent.html',{
                'user': user,
                'domain': current_site.domain,
                'login':'https://'+current_site.domain+'/auth/login',
                'image': 'http://'+current_site.domain+'/static/images/logo.jpg',}
            )

            email = EmailMultiAlternatives(
                            mail_subject, message, to=[email]
                )
            email.content_subtype = 'html'
            email.mixed_subtype = 'related'
            email.send()
            # print('working')
            return render(request,"email/confirm.html")
    return render(request, 'registration/signup.html', {'form': signup})

@login_required(login_url='/auth/login')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    profForm = profileForm()
    addrForm = addressForm()
    if request.method == 'POST':
        profForm = profileForm(request.POST,request.FILES,instance=request.user.profile)
        addrForm = addressForm(request.POST)
        if profForm.is_valid():
            user = User.objects.get(username=request.user.username)
            user.username = profForm.cleaned_data.get('username')
            user.first_name=profForm.cleaned_data.get('firstname')
            user.last_name=profForm.cleaned_data.get('lastname')
            user.save()
            profForm.save()
        if addrForm.is_valid():
            addr = Address.objects.filter(user=request.user).delete()
            address=addrForm.save(commit=False)
            address.user = request.user
            address.save()
        return render(request,'profile/profile.html',{"profile":profile,"profForm":profForm,"addrForm":addrForm})
    return render(request,'profile/profile.html',{"profile":profile,"profForm":profForm,"addrForm":addrForm})


def forgot_password(request):
    passwordForm = changePasswordForm()
    if request.method == 'POST':
        passwordForm = changePasswordForm(request.POST)
        if passwordForm.is_valid():
            username = passwordForm.cleaned_data.get('username')
            user = User.objects.get(username=username)
            if user:
                current_site = get_current_site(request)
                mail_subject = "Duka Discount Change Password"
                message = render_to_string('email/password.html',{
                    'user': request.user,
                    'domain': current_site.domain,
                     'link': 'http://'+current_site.domain+'/change/pass/',
                    'image': 'http://'+current_site.domain+'/static/images/logo.jpg',

                    }
                )

                email = EmailMultiAlternatives(
                                mail_subject, message, to=[user.email]
                    )
                email.content_subtype = 'html'
                email.mixed_subtype = 'related'
                email.send()
                return HttpResponse("Login to your Email")
    return render(request,"registration/change.html",{"form":passwordForm})


def search_results(request):
    if 'search' in request.GET and request.GET["search"]:
        search_term = request.GET.get("search")
        searched_items = Item.objects.filter(name__icontains=search_term)
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"category": searched_items})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


def items(request,pk):
    date = dt.date.today()
    post=Item.objects.get(id=pk)
    items = Item.objects.all()[1:5]
    return render(request,'each_item.html',{"posts":post,"date":date,"items":items})

@login_required(login_url='/auth/login/')
def add_to_cart(request,pk):
    post = Item.objects.get(id=pk)
    cart = Cart(user=request.user, item=post)
    saveToCart(cart, request)
    items = Cart.objects.filter(user=request.user)
    totalprice = 0
    for item in items:
        totalprice+=item.item.price
    return render(request,'cart.html',{"items":items, "totalprice":totalprice})

def saveToCart(cart, request):
    cart.save()
    orderItems = Order(user=request.user, item=cart.item)
    if cart.checkOutId:
        orderItems.checkOutId = cart.checkOutId
    orderItems.save()

@login_required(login_url='/auth/login/')
def removeItem(request,pk):
    post = Cart.objects.filter(id=pk).delete()
    # orderItems = Order.objects.filter(item=post.item).delete()
    items = Cart.objects.filter(user=request.user)
    return render(request,'cart.html',{"items":items})

@login_required(login_url='/auth/login/')
def viewcart(request):
    items = Cart.objects.filter(user=request.user)
    totalprice = 0
    for item in items:
        totalprice+=item.item.price
    return render(request,'cart.html',{"items":items,"totalprice":totalprice})

@login_required(login_url='/auth/login/')
def viewOrders(request):
    items = Order.objects.filter(user=request.user)
    totalprice = 0
    for item in items:
        totalprice+=item.item.price
    return render(request,'order.html',{"items":items,"totalprice":totalprice})

@login_required(login_url='/auth/login/')
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            # update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

@login_required(login_url='/auth/login')
def chat(request, pk):
    message_form = chatForm()
    user = User.objects.get(id=pk)
    messages = Messages.objects.all()
    texted_users = []
    for mess in messages:
        if mess.receive == request.user:
            if mess.sender not in texted_users:
                texted_users.append(mess.sender)

    if request.method == 'POST':
        message_form = chatForm(request.POST)
        if message_form.is_valid():
            messaging = message_form.save(commit=False)
            messaging.sender = request.user
            messaging.receive = user
            messaging.save()
            return redirect('chat',pk=pk)
    return render(request,'chat.html',{'chatform':message_form,"messages":messages,"user":user,
        "count":len(messages),
        "users":texted_users
          })

def category_item(request,keyword):
    items = Item.objects.filter(category__category__icontains=keyword)
    return render(request, 'category.html',{"items":items,"keyword":keyword})

@login_required(login_url='/auth/login')
def addnewsletter(request,code):
    if code == 1:
        mail = request.user.email
        newMail = newsLetter(email=mail)
        newMail.save()
        return redirect('profile')
    else:
        mail = newsLetter.objects.filter(email=request.user.email)
        mail.dele()
        return redirect('profile')



def getAccessToken():
    consumer_key = '3EtBE7ik2FXThAzN2EveWTKUdgAfnVs1'
    consumer_secret = 'AFdHFV89kpA8W08q'
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    print(mpesa_access_token)
    return validated_mpesa_access_token

def sanitiseNumber(phone):
    phone = str(phone)
    if phone.startswith("7"):
        string_number="254"+phone
        return int(string_number)
    elif phone.startswith("0"):
        list_number = list(str(phone))
        list_number[0] = "254"
        return int("".join(list_number))
    elif phone.startswith("+"):
        list_number = list(str(phone))
        list_number.pop(0)
        return int("".join(list_number))



def lipa_na_mpesa_online(request, amount):
    access_token = getAccessToken()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    stkPushrequest = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code, #587568
        "PhoneNumber": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "CallBackURL": "https://{}/confirmation/".format(get_current_site(request)),
        "AccountReference": str(request.user.username),
        "TransactionDesc": request.user + "Cart checkout"
    }
    response = requests.post(api_url, json=stkPushrequest, headers=headers)
    TransactionRequests.objects.filter(user=request.user).delete()
    print("statuscode: " + str(response.status_code))
    if response.status_code == 200:
        cartItems = Cart.objects.filter(user=reqeust.user)
        data = response.json()
        if 'ResponseCode' in data.keys():
            if data['ResponseCode'] == 0:
                merchant_id = data['MerchantRequestID']
                for carItem in cartItems:
                    cartItem.checkOutId = merchant_id
                    saveToCart(cartItem)
        pass
    merchant_id = response
    print(response.json())
    return redirect("/")



@csrf_exempt
def register_urls(request):
    access_token = getAccessToken()
    api_url = "https://api.safaricom.co.ke/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": WthdrawalsMpesaCreds.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://{}/confirmation/".format(get_current_site(request)),
               "ValidationURL": "https://{}/validation/".format(get_current_site(request))}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    print("called withdrawal")
    mpesa_body =request.body.decode('utf-8')
    print(mpesa_body)
    try:
        mpesa_payment = json.loads(mpesa_body)
        print(mpesa_payment)
    except Exception as e:
        print(e)
        context = {
            "ResultCode": 1,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))
    # print(mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'])
    if mpesa_payment['Body']['stkCallback']['ResultCode']==0:
        print(request.user)
        profile = Profile.objects.get(phone_number = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value'])
        transaction = Transactions(
           user = profile.user,
           phone = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value'],
           amount = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
           MpesaReceipt = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
           checkoutRequestId = mpesa_payment['Body']['stkCallback']['CheckoutRequestID'],
           status = "Success",
           direction="in"
       )
        transaction.save()
        orders = Order.objects.filter(checkOutId =
            mpesa_payment['Body']['stkCallback']['MerchantRequestID'])
        for order in orders:
            order.isPaidFor = True
            order.save()
        print("callback reg user profile")
        return redirect("/")
    transaction = Transactions(status=mpesa_payment['Body']['stkCallback']['ResultDesc'])
    print("failed")
    return redirect("/")