from essentials.models import Category

def categories(request):
    parent_categories = Category.objects.filter(parent__isnull=True, active=True)
    print(len(parent_categories), 'kac tane parent cat var')
    return {'parent_categories': parent_categories}