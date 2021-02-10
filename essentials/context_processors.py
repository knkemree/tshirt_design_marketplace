from essentials.models import Category, Product
from essentials.forms import SearchForm

def categories(request):
    parent_categories = Category.objects.filter(parent__isnull=True, active=True)
    return {'parent_categories': parent_categories}

def search_form(request):
    search_form = SearchForm()
    return {'search_form':search_form}