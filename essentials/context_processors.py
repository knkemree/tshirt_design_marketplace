from essentials.models import Category, Product

def categories(request):
    parent_categories = Category.objects.filter(parent__isnull=True, active=True)
    return {'parent_categories': parent_categories}

