from essentials.models import Category, Product

def categories(request):
    parent_categories = Category.objects.filter(parent__isnull=True, active=True)
    return {'parent_categories': parent_categories}

def latest_products(request):
    latest_products = Product.objects.filter(active=True)[:4]
    print(latest_products, 'en son urunler')
    return {'latest_products':latest_products}