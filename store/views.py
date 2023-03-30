from django.db.models import F, Sum
from django.utils import timezone
from decimal import Decimal
import decimal
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from .forms import *
from .cart import Cart
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.http import JsonResponse

def custom_login(username, password):
    user = authenticate(username=username, password=password)
    if user:
        return user
    return None

def login_view(request):
    if request.method == 'POST':
        # Validate the form data and authenticate the user
        username = request.POST['username']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(username=username)
            if customer.check_password(password):
                # Set the user's ID in the session and redirect to the dashboard
                request.session['_auth_user_id'] = customer.id
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create a new Customer instance from the form data
            customer = Customer(
                username=form.cleaned_data.get("username"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                email=form.cleaned_data.get("email"),
                shipping_address_1=form.cleaned_data.get("shipping_address_1"),
                shipping_address_2=form.cleaned_data.get("shipping_address_2"),
                shipping_city=form.cleaned_data.get("shipping_city"),
                shipping_state=form.cleaned_data.get("shipping_state"),
                shipping_zip_code=form.cleaned_data.get("shipping_zip_code"),
                shipping_country=form.cleaned_data.get("shipping_country"),
            )
            customer.set_password(form.cleaned_data.get("password"))
            customer.save()
            user = authenticate(username=form.cleaned_data.get("username"),
                                password=form.cleaned_data.get("password"))
            return redirect("login")
            
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def Home(request):
    #Authentication Cocki
    if '_auth_user_id' not in request.session:
        return redirect('login')

    products = Product.objects.all()
    cart = Cart(request)
    context = {
        'products':products,
        'cart':cart,
    }

    return render(request, 'index.html', context)

def ProductDetails(request, id):
    #Authentication Cocki
    if '_auth_user_id' not in request.session:
        return redirect('login')
    product = get_object_or_404(Product, id=id)
    
    context = {
        'product':product,
    }
    return render(request, 'product_details.html', context)

def cart(request):
    if '_auth_user_id' not in request.session:
        return redirect('login')
    customer = Customer.objects.get(id=request.session['_auth_user_id'])
    
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart, 'customer': customer})


def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'image': str(product.image),
        'category': str(product.category),
        'specifications': product.specifications,
        'quantity': product.quantity,
    }



def add_to_cart(request, product_id):
    if '_auth_user_id' not in request.session:
        return redirect('login')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity')
    update = request.POST.get('update')
    cart.add(product=product, quantity=quantity, update_quantity=update)
    cart_item = cart.cart[str(product.id)]
    cart_item['product'] = product_to_dict(product)
    return redirect('cart')

def remove_from_cart(request, product_id):
    if '_auth_user_id' not in request.session:
        return redirect('login')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart')

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def checkout(request):
    if '_auth_user_id' not in request.session:
        return redirect('login')
    cart = Cart(request)
    if request.method == 'POST':
        # Get customer information from form
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        payment_data = request.POST.get('payment_data')

        # Create a new order
        customer = Customer.objects.get(id=request.session['_auth_user_id'])
        print(cart)
        order = Order(customer=customer,
                      product_id=cart.get_items(),
                      shipping_address=shipping_address,
                      order_total=Decimal(str(cart.get_total_price())),
                      payment_method=payment_method,
                      payment_data=payment_data)
                      
        order.save()
        # Clear the cart and redirect to the order confirmation page
        cart.clear()
        return redirect('order_confirmation')

    return render(request, 'checkout.html', {'cart': cart})


def order_confirmation(request):
    if '_auth_user_id' not in request.session:
        return redirect('login')

    customer = Customer.objects.get(id=request.session['_auth_user_id'])
    latest_order = ustomer.order_set.latest('order_date')
    
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        # Update product quantity and revenue
        cart = request.session.get(settings.CART_SESSION_ID)
        if cart:
            # Fetch or create the Revenue object for the current date
            today = timezone.now().date()
            revenue, created = Revenue.objects.get_or_create(date=today)

            # Initialize the total_revenue field to 0 if it doesn't exist
            if created:
                revenue.total_revenue = Decimal(0)

            # Update the total_revenue field with the revenue generated by the current order
            for item_id in cart.keys():
                product = Product.objects.get(id=item_id)
                quantity = cart[item_id]['quantity']
                Product.objects.filter(id=product.id).update(quantity=F('quantity') - quantity)
                revenue.total_revenue += Decimal(cart[item_id]['price']) * quantity

            # Save the Revenue object
            revenue.save()
        order.fulfilled = True
        order.save()

        if cart:
            del request.session[settings.CART_SESSION_ID]

        return redirect('home')

    return render(request, 'order_confirmation.html', {'order': latest_order, 'customer': customer})

# from django.db.models import Sum
# from datetime import date, timedelta

# # Calculate revenue for the current month
# today = date.today()
# start_of_month = date(today.year, today.month, 1)
# end_of_month = start_of_month + timedelta(days=32 - start_of_month.day)

# revenue_for_month = Revenue.objects.filter(date__gte=start_of_month, date__lt=end_of_month).aggregate(total_revenue=Sum('total_revenue'))['total_revenue']

def profile(request):
    # Authentication check
    if '_auth_user_id' not in request.session:
        return redirect('login')
    
    # Get the customer instance
    customer = Customer.objects.get(id=request.session['_auth_user_id'])
    
    # Get the orders for the customer and order them by the date they were created
    orders = Order.objects.filter(customer=customer).order_by('-order_date')

    context = {'orders': orders}
    return render(request, 'profile.html', context)