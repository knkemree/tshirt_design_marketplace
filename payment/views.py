import stripe
from decouple import config
from django.views.decorators.debug import sensitive_variables
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import mail_admins
#from .tasks import payment_completed
from orders.models import Order


stripe.api_key = config('STRIPE_PRIVATE_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

# instantiate Stripe payment gateway
@sensitive_variables('token')
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    print("musterinin odedigi miktari gosteriyor dogru mu diye kontrol et")
    print(total_cost)
    if request.method == 'POST':
        # retrieve token
        token = request.POST.get('stripeToken')
        print("token burda")
        print(token)
        # create and submit transaction
        result = stripe.Charge.create(
            #amount=100,
            amount=int(total_cost*100),
            currency="usd",
            source=token,
            description="Payment for Context Custom",
        )
        print("result burda")
        print(result)
        if result.status == "succeeded":
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.stripe_id = result.id
            order.save()
            subject = "New Order"
            message = "Order"
            mail_admins(subject, message, html_message="We got new order. Go to orders: contextcustom.com/admin/orders/order/")
            # launch asynchronous task
            # payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        return render(request,
                      'process.html',
                      {'order': order,
                       'publish_key':STRIPE_PUBLIC_KEY})

def payment_done(request):
    return render(request, 'done.html')
def payment_canceled(request):
    return render(request, 'canceled.html')
