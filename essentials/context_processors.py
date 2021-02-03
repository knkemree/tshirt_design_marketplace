from essentials.models import Category

def categories(request):
    parent_categories = Category.objects.filter(parent__isnull=False)
    return {'parent_categories': parent_categories}