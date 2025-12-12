import razorpay
from django.conf import settings
from django.shortcuts import render,redirect
from .models import  *
from django.contrib import messages

# Create your views here.

def indexpage(request):

    products = newproductmodel.objects.all()
    refurbishedproducts = refurbishedproductmodel.objects.all()

    print(products)
    print(refurbishedproducts)

    context = {
        "products": products,
        "product": refurbishedproducts


    }

    return render(request,"index.html",context)
def fetchregister(request):
    name=request.POST.get("user-name")
    email = request.POST.get("user-email")
    password= request.POST.get("user-password")
    phone=request.POST.get("user-phone")

    print(name)
    print(email)
    print(password)
    print(phone)

    insertquery=registermodel(name=name,email=email,password=password,phone=phone)
    insertquery.save()
    print("success")

    return render(request, "login.html")

def fetchlogin(request):
    #form to variable
    

    uname=request.POST.get("user-name")
    upassword = request.POST.get("user-password")

    print(uname)
    print(upassword)

    try:
        userdata = registermodel.objects.get(name=uname, password=upassword)
        print(userdata)

        # session start
        request.session["log_id"] = userdata.id
        request.session["log_name"] = userdata.name
        request.session["log_email"] = userdata.email
    except:
        print("failure")
        userdata = None

    if userdata is not None:
        return render(request, "index.html")
    else:
        print("invaild email or password")
        messages.error(request, "Invaild email or password")
    return render(request, "login.html")

def logout(request):
    try:
        del request.session["log_id"]
        del request.session["log_name"]
        del request.session["log_email"]
    except:
        pass
    return render(request, "index.html")



def fetchadddata(request):
    name=request.POST.get("name")
    categoryid =request.POST.get("category")
    price=request.POST.get("price")
    image=request.FILES["dp"]
    description= request.POST.get("description")
    status= request.POST.get("status")

    # user id from sessiom
    userid = request.session["log_id"]

    print(name)
    print(categoryid)
    print(price)
    print(description)
    print(status)

    newquery = newproductmodel(name=name,category=category(id=categoryid),price=price,image=image,description=description, status=status,userid=registermodel(id=userid))
    newquery.save()
    print("success")
    return render(request, "index.html")


def shop3(request):
    refurbishedproducts = refurbishedproductmodel.objects.all()
    context = {
        "products": refurbishedproducts
    }
    return render(request,"shop-3-column.html",context)

def shop4(request):
    products = newproductmodel.objects.all()


    context = {
        "products": products,


    }
    return render(request,"shop-4-column.html", context)




def productpage(request):
    # fetch cat data
    fetchcategory = category.objects.all()
    context = {
        "categorydata": fetchcategory
    }
    return render(request,"product.html",context)

def loginpage(request):
    return render(request,"login.html")

def addproductpage(request):
    return render(request,"addproduct.html")
def newpage(request):
    return render(request,"new.html")


def cartpage(request):
    try:
        userid = request.session["log_id"]
        fetchdata = cart.objects.filter(userid=userid,orderstatus=1)
        total=sum(item.totalamount for item in fetchdata)

        context = {
            "data": fetchdata,
            "total":total
        }
    except:
        return redirect(loginpage)
    return render(request,"cart.html",context)

def placeorder(request):
    uid = request.session.get("log_id")
    total = request.POST.get("total")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    payment_method = request.POST.get("payment")
    user = registermodel.objects.get(id=uid)

    if payment_method == "Cash on Delivery":
        storedata = ordermodel( userid=user,finaltotal=total, phone=phone, status=True  ,address=address, paymode="Cash on Delivery" )
        storedata.save()
        lastid = storedata.id
        # Update Cart Items
        cart_items = cart.objects.filter(userid=uid,orderstatus=1)
        for item in cart_items:
            item.orderstatus = 0
            item.orderid = lastid
            item.save()
            product = None

            # if item.productid:
            #     product = item.productid
            # elif item.rproductid:
            #     product = item.rproductid
            #
            # if product:
            #     product.status=Unavailable
            #
            #     product.save()


        return redirect("/")

    else:
        client =razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_SECRET_KEY))
        order_amount = int(float(total) * 100)  # Razorpayneedsamount in paise
        razorpay_order = client.order.create({
            "amount": order_amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{uid}",
            "payment_capture": "1",
        })
    storedata = ordermodel(
        userid=user,
        finaltotal=total,
        phone=phone,
        address=address,
        status=True,
        paymode="Online",
        razorpay_order_id=razorpay_order['id'],
    )
    storedata.save()
    lastid = storedata.id
    # Update Cart Items
    cart_items = cart.objects.filter(userid=uid,orderstatus=1)
    for item in cart_items:
        item.orderstatus = 0
        item.orderid = lastid
        item.save()
        product = None

        # if item.productid:
        #     product = item.productid
        # elif item.rproductid:
        #     product = item.rproductid
        #
        # if product:-
        #     product.status = False
        #     product.save()

        return render(request, "payment.html", {
            "razorpay_order_id": razorpay_order['id'],
            "amount": order_amount,
            "key": settings.RAZORPAY_KEY_ID,
            "currency": "INR",

        })


def insertintocart(request):
    userid = request.session["log_id"]
    pid = request.POST.get("pid")
    price = request.POST.get("price")
    quantity = request.POST.get("quantity")
    totalamount = float(price) * int(quantity)

    insertquery = cart(userid=registermodel(id=userid), productid=newproductmodel(id=pid), quantity=quantity,totalamount=totalamount, orderstatus=1, orderid=0)
    insertquery.save()
    messages.success(request, "Product Added to Cart")
    return redirect("/shop-4-column")

def aboutpage(request):
    return render(request,"about.html")


def deleteitem(request,id):
    print(id)
    # delete query
    # delete from tablename where id=id
    fetchdata = cart.objects.get(id=id)
    fetchdata.delete()
    messages.success(request,"Product Deleted")
    return redirect("/cart")
def myaccountpage(request):
    uid = request.session["log_id"]
    rdata = registermodel.objects.get(id=uid)
    fetchdata = ordermodel.objects.filter(userid=rdata)
    context = {
        'data':fetchdata
    }
    return render(request,"my-account.html",context)


def search_product_view(request):
    query = request.GET.get("query")

    # Check in refurbished products
    product = refurbishedproductmodel.objects.filter(name__iexact=query).first()
    if product:
        return redirect(single_product_variablepage, id=product.id)

    # Check in new products
    product = newproductmodel.objects.filter(name__iexact=query).first()
    if product:
        return redirect(single_productpage, id=product.id)

    # If not found
    return redirect("/")

def yourordersingle(request,id):
    fetchdata = cart.objects.filter(orderid=id)
    context = {
        'data':fetchdata
    }
    return render(request,"yourordersingle.html",context)

def contactpage(request):
    return render(request,"contact.html")
def contactfetch(request):
    name=request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    # pid = request.POST.get("message")
    print(name)
    print(email)
    print(message)
    print(subject)
    userid = request.session["log_id"]



    insertquery = contact_us(name=name, email=email, subject=subject, message=message,userid=registermodel(id=userid))
    insertquery.save()
    print("success")

    return render(request, "index.html")




def single_productpage(request,id):
    print(id)
    fetchdata = newproductmodel.objects.get(id=id)
    context = {
        "data": fetchdata
    }
    return render(request, "single-product.html", context)


def single_product_variablepage(request,id):
    print(id)
    # fetch single data query
    # select * from product where id=id
    fetchdata = refurbishedproductmodel.objects.get(id=id)
    context = {
        "data": fetchdata
    }
    return render(request,"single-product-variable.html",context)





def insertintocartrefurbish(request):
    userid = request.session["log_id"]
    pid = request.POST.get("pid")
    price = request.POST.get("price")
    quantity = request.POST.get("quantity")
    totalamount = float(price) * int(quantity)

    insertquery = cart(userid=registermodel(id=userid), rproductid=refurbishedproductmodel(id=pid), quantity=quantity,totalamount=totalamount, orderstatus=1, orderid=0)
    insertquery.save()
    messages.success(request, "Product Added to Cart")

    return redirect("/shop-3-column")

def manageproductpage(request):
    user_logged = request.session["log_id"]
    fetchdata = newproductmodel.objects.filter(userid=user_logged)
    context = {
        "data": fetchdata
    }
    return render(request,"manageproduct.html",context)

def deletepage(request,id):
    print(id)
    fetchdata=newproductmodel.objects.get(id=id)
    fetchdata.delete()
    messages.success(request,"product delete")
    return redirect("/manageproduct")

def editproduct(request,id):
    fetchdata = newproductmodel.objects.get(id=id)
    fetchcat = category.objects.all()
    context = {
        "data": fetchdata,
        "category": fetchcat
    }
    return render(request,"editproduct.html",context)

def updateproduct(request):
    name = request.POST.get("name")
    categoryid = request.POST.get("category")
    price = request.POST.get("price")
    image = request.FILES["dp"]
    description = request.POST.get("description")
    status = request.POST.get("status")
    pid=request.POST.get("pid")

    # user id from sessiom
    userid = request.session["log_id"]

    # update table set name=name , price=price where id=pid
    fetchdata = newproductmodel.objects.get(id=pid)
    fetchdata.name = name
    fetchdata.category = category(id=categoryid)
    fetchdata.image = image
    fetchdata.price = price
    fetchdata.description = description
    fetchdata.status = status
    fetchdata.userid = registermodel(id=userid)
    fetchdata.save()
    messages.success(request, "Data Updated")

    return redirect("/manageproduct")

def updatelogin(request):
    # form to variable

    uname = request.POST.get("user-name")
    upassword = request.POST.get("user-password")
    npassword=request.POST.get("user-npassword")
    try:
        fetchdata = registermodel.objects.get(name=uname,password=upassword)
        fetchdata.password = npassword
        fetchdata.save()
        messages.success(request, "Password Change successfully")
    except:
        messages.error(request, "Password Does Not Change")

    return redirect("/login")

def editlogin(request):

    return render(request,"editlogin.html")

def payment_success(request):
    return render(request, "shop-4-column.html")




