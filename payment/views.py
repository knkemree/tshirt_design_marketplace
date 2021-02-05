import stripe
from decouple import config
from django.views.decorators.debug import sensitive_variables
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import mail_admins
#from .tasks import payment_completed
from orders.models import Order
from cart.cart import Cart



stripe.api_key = config('STRIPE_PRIVATE_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

# instantiate Stripe payment gateway
@sensitive_variables('token')
def payment_process(request):
    cart = Cart(request)
    
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    credit = order.ordered_by.credit
        

    if request.method == 'POST' and total_cost >= credit:
        after_credit = total_cost-credit
        
        # retrieve token
        token = request.POST.get('stripeToken')
        # create and submit transaction
        result = stripe.Charge.create(
            #amount=100,
            amount=int(after_credit*100),
            currency="usd",
            #customer = order.ordered_by.seller.seller.stripe_id,
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
            subject = "New Order"
            message = "Order"
            mail_admins(subject, message, html_message="{} has just placed an order. <a href='https://contextcustom.com/admin/orders/order/{}/change/'>Check Now!</a>".format(order.customer_name(), order.id))
            
             
            
            del request.session['order_id']
            request.session.modified = True


            order.ordered_by.credit = 0 
            #credit_record = Credit.objects.create(user=order.ordered_by, order_id=order.id, amount=credit*-1)
            order.save()
            order.ordered_by.save()
            #credit_record.save()
            print(after_credit, 'ne kadar charge edildi')
            # cart.clear()
            # launch asynchronous task
            # payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            del request.session['order_id']
            request.session.modified = True
            return redirect('payment:canceled')
    else:

        if request.method == 'POST' and total_cost < credit:
            after_credit = 0.00
            subject = "New Order"
            message = "Order"
            mail_admins(subject, message, html_message="{} has just placed an order. <a href='https://contextcustom.com/admin/orders/order/{}/change/'>Check Now!</a>".format(order.customer_name(), order.id))
            del request.session['order_id']
            request.session.modified = True

            
            order.paid = True

            order.ordered_by.credit = credit - total_cost
            #credit_record = Credit.objects.create(user=order.ordered_by, order_id=order.id, amount=total_cost*-1)
            #credit_record.save()
            order.save()
            order.ordered_by.save()
            return redirect('payment:done')
        
        else:
            if total_cost >= credit:
                after_credit = total_cost-credit
            else:
                after_credit = 0.00
            return render(request,
                      'process.html',
                      {'order': order,
                      'after_credit':after_credit,
                       'publish_key':STRIPE_PUBLIC_KEY})

def payment_done(request):
    return render(request, 'done.html')
def payment_canceled(request):
    return render(request, 'canceled.html')


def pay_order(request, id):
    order = get_object_or_404(Order, id=id)
    total_cost = order.get_total_cost()

    credit = order.ordered_by.credit
        

    if request.method == 'POST' and total_cost >= credit:
        after_credit = total_cost-credit
        
        # retrieve token
        token = request.POST.get('stripeToken')
        # create and submit transaction
        result = stripe.Charge.create(
            #amount=100,
            amount=int(after_credit*100),
            currency="usd",
            #customer = order.ordered_by.seller.seller.stripe_id,
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
            subject = "Order Paid"
            message = "Order"
            mail_admins(subject, message, html_message="{} has just made a payment for order #{}. <a href='https://contextcustom.com/admin/orders/order/{}/change/'>Check Now!</a>".format(order.customer_name(), order.id, order.id))


            order.ordered_by.credit = 0 
            #credit_record = Credit.objects.create(user=order.ordered_by, order_id=order.id, amount=credit*-1)
            order.save()
            order.ordered_by.save()
            #credit_record.save()
            print(after_credit, 'ne kadar charge edildi')
            # cart.clear()
            # launch asynchronous task
            # payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:

        if request.method == 'POST' and total_cost < credit:
            after_credit = 0.00
            subject = "Order Paid"
            message = "Order"
            mail_admins(subject, message, html_message="{} has just made a payment for order #{}. <a href='https://contextcustom.com/admin/orders/order/{}/change/'>Check Now!</a>".format(order.customer_name(), order.id, order.id))

            
            order.paid = True

            order.ordered_by.credit = credit - total_cost
            #credit_record = Credit.objects.create(user=order.ordered_by, order_id=order.id, amount=total_cost*-1)
            #credit_record.save()
            order.save()
            order.ordered_by.save()
            return redirect('payment:done')
        
        else:
            if total_cost >= credit:
                after_credit = total_cost-credit
            else:
                after_credit = 0.00
            return render(request,
                      'pay_in_order_history.html',
                      {'order': order,
                      'after_credit':after_credit,
                       'publish_key':STRIPE_PUBLIC_KEY})