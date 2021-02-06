from PIL import Image
import base64, secrets, io
#import weasyprint
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from account.models import Seller
from essentials.models import Design
import weasyprint
from django.core.mail import mail_admins


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + '/css/pdf.css')])
    return response



#def get_image_from_data_url(data_url, resize=True, base_width=600 ):
def get_image_from_data_url(data_url, resize=True, base_width=1200):

    # getting the file format and the necessary dataURl for the file
    _format, _dataurl       = data_url.split(';base64,')
    # file name and extension
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]

    # generating the contents of the file
    file = ContentFile(base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    # resizing the image, reducing quality and size
    if resize:

        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        # resize
        #w_percent    = (base_width/float(image.size[0]))
        #h_size       = int((float(image.size[1])*float(w_percent)))
        #image        = image.resize((base_width,h_size), Image.ANTIALIAS)

        # save resized image
        image.save(image_io, format=_extension)

        # generating the content of the new image
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" )

    # file and filename
    return file, ( _filename, _extension )

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            email = Seller.objects.get(seller=request.user)
            order.ordered_by = email 
            order.total = cart.get_total_price()
            order = form.save(commit=False)
            # if cart.coupon:
            #     order.coupon = cart.coupon
            #     order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                end_product_img = get_image_from_data_url(item['end_product_img'])[0]
                image = get_image_from_data_url(item['design'])[0]
                OrderItem.objects.create(order=order,
                                        variant_id=item['variant_id'],
                                        price=item['price'],
                                        end_product_img=end_product_img,
                                        image = image,
                                        quantity=item['quantity'],
                                        technique=item['technique'],
                                        placement = item['placement'],
                                        json_data = item['json_data']
                                        )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            try:
              order_created.delay(order.id)
            except:
              pass
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'create.html',
                  {'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

@staff_member_required
def admin_order_item_detail(request, order_id):
    order_item = get_object_or_404(OrderItem, id=order_id)
    return render(request,
                  'admin/orders/orderitem/detail.html',
                  {'order_item': order_item})

@login_required
def order_list(request):
    seller = Seller.objects.get(seller=request.user)
    orders = Order.objects.filter(ordered_by=seller)
    context = {
        'seller':seller,
        'orders': orders,
    }
    return render(request, 'order_list.html', context)

def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    def cancel_apply_credit(order_instance):
        order.status = '4'
        order.ordered_by.credit = order.ordered_by.credit + order.total
        order.save()
        order.ordered_by.save()
    def cancel_do_not_apply_credit(order_instance):
        order.status = '4'
        order.save()

    def notify_admins(order_instance):
        subject = "Order #{} Cancelled".format(order.id)
        message = "Order"
        mail_admins(subject, message, html_message="{} has cancelled order #{}. <a href='https://contextcustom.com/admin/orders/order/{}/change/'>Check Now!</a>".format(order.customer_name(), order.id, order.id))

    if order.paid:
        cancel_apply_credit(order)
        notify_admins(order)
    else:
        cancel_do_not_apply_credit(order)
        notify_admins(order)

    
    return redirect('orders:order_list')