from django.shortcuts import get_object_or_404
from account.models import Customer, Seller

def credit_amount(request):
    seller = get_object_or_404(Seller, seller=request.user)
    credit_amount = seller.credit
    print(credit_amount, 'ne kadar kredisi var')
    return {'credit_amount':credit_amount}