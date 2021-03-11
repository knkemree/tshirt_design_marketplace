import stripe
from decimal import Decimal
from decouple import config
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_variables
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import mail_admins
#from .tasks import payment_completed
from orders.models import Order
from cart.cart import Cart
from account.models import Credit, Seller



stripe.api_key = config('STRIPE_PRIVATE_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

# instantiate Stripe payment gateway
@sensitive_variables('token')
def payment_process(request):
    cart = Cart(request)

    #eger order'i bulamazsa order list'e geri don. order'i bulamamasinin sebebi session'dan order_id'nin silinmesi olabilir
    try:
        order_id = request.session.get('order_id')
        order = Order.objects.get(id=order_id)
    except:
        return redirect("orders:order_list")

    total_cost = order.get_total_cost()
    credit = order.ordered_by.credit
        

    if request.method == 'POST' and total_cost > credit:
        after_credit = total_cost-credit
        
        # retrieve token
        token = request.POST.get('stripeToken')
        # create and submit transaction
        try:
            result = stripe.Charge.create(
                #amount=100,
                amount=int(after_credit*100),
                currency="usd",
                #customer = order.ordered_by.seller.stripe_id,
                source=token,
                description="Customer:{}, Order #{}, Total:${}, Used credit:${}, Paid Amount: ${}".format(order.ordered_by, order.id, total_cost, credit, after_credit),
            )
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.stripe_id = result.id
            subject = "New Order"
            message = "Order"
            mail_admins(subject, message, html_message="{} has just placed an order. <a href='https://contextcustom.com/admin/orders/order/{}/change/'>Check Now!</a>".format(order.customer_name(), order.id))
            order.ordered_by.credit = 0 
            order.save()
            order.ordered_by.save()
            # cart.clear()
            # launch asynchronous task
            # payment_completed.delay(order.id)
            del request.session['order_id']
            request.session.modified = True
            return redirect('payment:done')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect('payment:canceled')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "To many request error")
            return redirect('payment:canceled')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid Parameter")
            return redirect('payment:canceled')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Authentication with stripe failed")
            return redirect('payment:canceled')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network Error")
            return redirect('payment:canceled')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, "Something went wrong")
            return redirect('payment:canceled')
        
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(request, "Not identified error")

            return redirect('payment:canceled')

    else:

        if request.method == 'POST' and total_cost <= credit:
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


@login_required(login_url='/signup/')
def pay_order_done(request):
    return render(request, 'pay_order_done.html')

@login_required(login_url='/signup/')
def payment_done(request):
    return render(request, 'done.html')

@login_required(login_url='/signup/')
def payment_canceled(request):
    #eger order'i bulamazsa order list'e geri don. order'i bulamamasinin sebebi session'dan order_id'nin silinmesi olabilir
    try:
        order_id = request.session.get('order_id')
        order = Order.objects.get(id=order_id) 
        context = {'order_id':order.id}
        return render(request, 'canceled.html', context)
    except:
        return redirect("orders:order_list")

@login_required(login_url='/signup/')
def credit_payment_failed(request):
    return render(request, 'credit_payment_failed.html',)
    
    


@login_required(login_url='/signup/')
def pay_order(request, id):
    order = get_object_or_404(Order, id=id)
    total_cost = order.get_total_cost()
    credit = order.ordered_by.credit
    if request.method == 'POST' and total_cost > credit:
        after_credit = total_cost-credit
        
        # retrieve token
        token = request.POST.get('stripeToken')
        try:
            result = stripe.Charge.create(
                #amount=100,
                amount=int(after_credit*100),
                currency="usd",
                #customer = order.ordered_by.seller.stripe_id,
                source=token,
                description="Customer:{}, Order #{}, Total:${}, Used credit:${}, Paid Amount: ${}".format(order.ordered_by, order.id, total_cost, credit, after_credit),
            )
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.stripe_id = result.id
            subject = "New Order"
            message = "Order"
            mail_admins(subject, message, html_message="{} has just placed an order. <a href='https://contextcustom.com/admin/orders/order/{}/change/'>Check Now!</a>".format(order.customer_name(), order.id))
            order.ordered_by.credit = 0 
            order.save()
            order.ordered_by.save()
            # cart.clear()
            # launch asynchronous task
            # payment_completed.delay(order.id)
            del request.session['order_id']
            request.session.modified = True
            return redirect('payment:done')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect('payment:canceled')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "To many request error")
            return redirect('payment:canceled')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid Parameter")
            return redirect('payment:canceled')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Authentication with stripe failed")
            return redirect('payment:canceled')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network Error")
            return redirect('payment:canceled')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, "Something went wrong")
            return redirect('payment:canceled')
        
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(request, "Not identified error")

            return redirect('payment:canceled')
    else:

        if request.method == 'POST' and total_cost <= credit:
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


@login_required(login_url='/signup/')
def pay_for_credit(request):
    amount = Decimal(request.session.get('amount')) #since decimal object is not json serializable i made i str in account:create_credit view and changed here to Decimal
    print(amount, 'amount burda')
    seller = get_object_or_404(Seller, seller_id=request.user.id)
    if request.method == 'POST' :

        # retrieve token
        token = request.POST.get('stripeToken')
        try:
            # create and submit transaction
            result = stripe.Charge.create(
                #amount=100,
                amount=int(int(amount)*100),
                currency="usd",
                #customer = order.ordered_by.seller.stripe_id,
                source=token,
                description="Customer uploaded money",
            )



            credit = Credit.objects.create(email=seller, added_amount=amount, created_by = 'seller')
            seller.credit = seller.credit + Decimal(credit.added_amount)
            seller.save()
            # store the unique transaction id
            credit.stripe_id = result.id
            credit.save()
            subject = "Credit Given"
            message = "Credit"
            mail_admins(subject, message, html_message="{} has just uploaded credits. <a href='https://contextcustom.com/admin/account/credit/{}/change/'>Check Now!</a>".format(credit.email, credit.id))
            del request.session['amount']
            request.session.modified = True
            return redirect('payment:done')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect('payment:credit_payment_failed')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "To many request error")
            return redirect('payment:credit_payment_failed')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid Parameter")
            return redirect('payment:credit_payment_failed')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Authentication with stripe failed")
            return redirect('payment:credit_payment_failed')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network Error")
            return redirect('payment:credit_payment_failed')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, "Something went wrong")
            return redirect('payment:credit_payment_failed')
        
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(request, "Not identified error")

            return redirect('payment:credit_payment_failed')
        
    elif amount == None:
            return redirect(reverse('orders:order_list'))
    else:
        return render(request,
                        'pay_for_credit.html',
                        {
                        'credit':amount,
                        'publish_key':STRIPE_PUBLIC_KEY})
