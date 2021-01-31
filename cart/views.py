from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from essentials.models import Design, Product, Variant
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from django.core.mail import mail_admins


@require_POST
def cart_add(request, variant_id, art_id=None):
    data = {}
    cart = Cart(request)
    print('cartta nee var')
    print(cart)
    print(variant_id)
    if request.method == 'POST':
        form = CartAddProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            # if not updating qty create new design instance
            if cd['override'] == False:
                art = Design.objects.create(email=request.user, variant_id=variant_id)
                art.save()
            #if updating get art.id from session. session created when first click on add to cart
            else:
                art = get_object_or_404(Design, id=art_id)
            cart.add(
                    art=art,
                    variant=art.variant,
                    placement = cd['placement'],
                    technique = cd['technique'],
                    quantity=cd['quantity'],
                    override_quantity=cd['override'],
                    end_product_img=cd['end_product_img'],
                    mockup = cd['mockup'],
                    design = cd['design'],
                    json_data = cd['json_data']
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
def cart_remove(request, art_id):
    cart = Cart(request)
    product = get_object_or_404(Design, id=art_id)
    cart.remove(product)
    product.delete()
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
    #return JsonResponse(data)

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponse('Cart cleared!')