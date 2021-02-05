from django.shortcuts import get_object_or_404
from account.models import Customer, Seller

def credit_amount(request):
    try:
        seller = Seller.objects.get(seller=request.user)
        credit_amount = seller.credit
        context = {'credit_amount':credit_amount}
        print(credit_amount, 'ne kadar kredisi var')
        return context
    except:
        return {'credit_amount':0}