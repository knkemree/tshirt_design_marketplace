from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from essentials.models import Product, Variant
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from django.core.mail import mail_admins


@require_POST
def cart_add(request, variant_id):
    data = {}
    cart = Cart(request)
    variant = get_object_or_404(Variant, id=variant_id)
    print('variant burda')
    print(variant)
    data['variant'] = variant.id
    if request.method == 'POST':
        form = CartAddProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(variant=variant,
                    quantity=cd['quantity'],
                    override_quantity=cd['override'],
                    end_product_img=cd['end_product_img'],
                    mockup = cd['mockup'],
                    design = cd['design']
                    )
            data['result'] = "Added to cart"
            return redirect('cart:cart_detail')
            #return JsonResponse(data)
        else:
            data['result'] = form.errors
            return redirect('cart:cart_detail')
            #return JsonResponse(data)
    data['result'] ='form not submitted yet' 
    return redirect('cart:cart_detail')
    #return JsonResponse(data)

@require_POST
def cart_remove(request, variant_id):
    cart = Cart(request)
    product = get_object_or_404(Variant, id=variant_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    coupon_apply_form = CouponApplyForm()
    context = {'cart': cart,
                'coupon_apply_form': coupon_apply_form}
    return render(request, 'cart.html', context)
    #return HttpResponse('hi')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    subject = "New Order"
    message = "Order"
    mail_admins(subject, message, html_message="we got new order. Go to orders: contextcustom.com/orders/order/")
    return HttpResponse('Cart cleared!')