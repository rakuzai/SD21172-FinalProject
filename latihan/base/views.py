import pandas as pd
import matplotlib.pyplot as plt
import io


from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Food, Order, Payment

# Create your views here.

def loginPage(request):

    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    return render(request, 'base/home.html')

def listMenu(request):
    foods = Food.objects.all()
    context = {'foods': foods}
    #if request.user.is_staff:
        #return HttpResponse('Anda tidak dapat mengakses halaman ini')
    return render(request, 'base/listMenu.html', context)

@login_required(login_url='login')
def create_order(request):
    if request.method == "POST":
        food_id = request.POST["food"]
        quantity = request.POST["quantity"]
        food = Food.objects.get(pk=food_id)
        order = Order.objects.create(
            user=request.user, 
            food=food, 
            quantity=quantity
        )
        return redirect("order_detail", pk=order.pk)
    else:
        food_list = Food.objects.all()
        return render(request, "base/create_order.html", {"food_list": food_list})

def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request, "base/order_detail.html", {"order": order})

def make_payment(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        amount = request.POST["amount"]
        is_payment_less = order.is_payment_less()
        if is_payment_less == False:
            payment = Payment.objects.create(order=order, amount=amount)
            return redirect("payment_receipt", pk=payment.pk)
        else:
            return HttpResponse("Pembayaran kurang dari total harga")
    else:
        return render(request, "base/make_payment.html", {"order": order})

def payment_receipt(request, pk):
    payment = Payment.objects.get(pk=pk)
    order = Order.objects.get(pk=payment.order.pk)
    is_payment_less = order.is_payment_less()
    context = {"payment": payment, "order": order, "is_payment_less": is_payment_less}
    return render(request, "base/payment_receipt.html", context)


@login_required(login_url='login')
def tampilGrafik(request):
    orders = Order.objects.all()
    data = []
    for order in orders:
        data.append({"user": order.user.username, "total_purchase": order.quantity})
    df = pd.DataFrame(data)
    df_group = df.groupby("user").sum().reset_index()
    df_group.plot(kind = 'bar', x = 'user', y = 'total_purchase')
    plt.xlabel("User")
    plt.ylabel("Total Penjualan")
    plt.title("Total Jumlah Penjualan Menu Berdasarkan User")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    response = HttpResponse(buf.read(), content_type='image/png')
    plt.close()
    return response
