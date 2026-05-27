from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm,UserRegistrationForm, UserLoginForm,BuyNowForm
from .models import Product
from .models import Seller, Product,Buyer
from django.contrib.auth.models import User
from .models import User 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
     
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm_password']
            role = form.cleaned_data.get('role', 'buyer')

            if password != confirm:
                return render(request, 'EcoWeb/register.html',
                              {'form': form, 'msg': 'Passwords do not match'})

            if User.objects.filter(username=email).exists():
                return render(request, 'EcoWeb/register.html',
                              {'form': form, 'msg': 'Email already registered'})

            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                role=role
            )
            if role == 'seller':
                Seller.objects.create(user=user, name=email.split('@')[0],email=email,phone='' )

          
            if role == 'buyer':
                Buyer.objects.create(
                    user=user,
                    product=form.cleaned_data.get('email'),  
                    address=form.cleaned_data.get('address'),
                    city=form.cleaned_data.get('city'),
                    state=form.cleaned_data.get('state'),
                    phone_number=form.cleaned_data.get('phone_number'),
                    delivery_instructions=form.cleaned_data.get('delivery_instructions'),
                    created_at=form.cleaned_data.get('created_at')
                )

            return redirect('login')

    else:
   

        form = UserRegistrationForm()

    return render(request, 'EcoWeb/register.html', {'form': form})
#########################

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password'] 

            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user) 
                return redirect('productlist')
            else:
                return render(request, 'EcoWeb/login.html', {
                    'form': form,
                    'msg': 'Invalid credentials'
                })
    else:
        form = UserLoginForm()

    return render(request, 'EcoWeb/login.html', {'form': form})
###################

def logout_view(request):
    logout(request)
    return redirect('login')

#####################

@login_required
def productlist(request):
    if hasattr(request.user, 'seller'):
    
        seller = Seller.objects.get(user=request.user)
        products = Product.objects.filter(seller=seller)
    else:
        
        products = Product.objects.all()
    return render(request, 'EcoWeb/productlist.html', {'products': products})

####################
@login_required
def product_create(request):
    if request.user.role != 'seller':
        return redirect('productlist')

    seller, created = Seller.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,
            'email': request.user.email,
            'phone': '',
        }
    )

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product.objects.create(
                seller=seller,
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price'],
                quantity=form.cleaned_data['quantity'],
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description']
            )
            return redirect('productlist')
    else:
        form = ProductForm()

    return render(request, 'EcoWeb/product_form.html', {'form': form, 'action': 'Create'})

####################

@login_required
def edit_product(request, pk):
   # seller = get_object_or_404(Seller, user=request.user)
    #product = get_object_or_404(Product, pk=pk, seller=seller)
    seller=Seller.objects.filter(user=request.user).first()
    if not seller:
        
        return redirect('productlist')
    product=Product.objects.filter(pk=pk,seller=seller).first()
    if not product:
        return redirect('productlist')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.price = form.cleaned_data['price']
            product.quantity = form.cleaned_data['quantity']
            product.image=form.cleaned_data['image']
            product.description = form.cleaned_data['description']

            product.save()
            return redirect('productlist')
    else:
        

        form = ProductForm(initial={
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'image':product.image,
            'description': product.description
        })
    return render(request, 'EcoWeb/product_form.html', {
        'form': form,
        'action':'Edit'
        })

######################

@login_required
def delete_product(request, pk):
    #seller = get_object_or_404(Seller, user=request.user)# jo user login hai uske basis pr seller find karna
    #product = get_object_or_404(Product, pk=pk, seller=seller)
    seller = Seller.objects.filter(user=request.user).first()

    if not seller:
        return redirect('productlist')

    product = Product.objects.filter(pk=pk, seller=seller).first()

    if not product:
        return redirect('productlist')

    if request.method == 'POST':
        product.delete()
        return redirect('productlist')

    return render(request, 'EcoWeb/delete.html', {'product': product})

###########
@login_required
def buyer_product(request, pk):
    
    product = Product.objects.get(pk=pk)

    if request.method == "POST":
        form = BuyNowForm(request.POST)
        if form.is_valid():
           
            Buyer.objects.create(
                user=request.user,
                product=product,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                phone_number=form.cleaned_data['phone_number'],
                delivery_instructions=form.cleaned_data.get('delivery_instructions')
            )
            return redirect('productlist')
    else:
        form = BuyNowForm()

    return render(request, 'EcoWeb/buyer.html', {'form': form, 'product': product})