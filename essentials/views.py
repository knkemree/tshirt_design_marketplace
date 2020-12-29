from django.shortcuts import render
from django.db.models import Q, Avg, Count
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from cart.forms import CartAddProductForm
from .models import Category, Product, Variant
from account.mixins import SellerAccountMixin



# Create your views here.
class SellerProductListView(SellerAccountMixin, ListView):
	model = Product
	template_name = "sellers_product_catalog.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(SellerProductListView, self).get_queryset(**kwargs)
		qs = qs.filter(seller=self.get_account())
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(detail__icontains=query)
				).order_by("title")
		return qs


@login_required(login_url='/signup/')
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(active=True)
    print(request.session.keys())
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    query = request.GET.get('q')
    product = get_object_or_404(Product,id=id,slug=slug,active=True)

    if request.method == 'POST':
        variant_id = request.POST.get('variantid')                                                                                                                                                  
        variant = Variant.objects.get(id=variant_id) #selected product by click color radio
        colors = Variant.objects.filter(product_id=id,size_id=variant.size_id )
        sizes = Variant.objects.filter(product_id = variant.product_id).order_by('size__id').distinct('size__id')
        query += variant.product.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
    else:
        variants = Variant.objects.filter(product_id=id)
        colors = Variant.objects.filter(product_id=id,size_id=variants[0].size_id )
        variant = Variant.objects.get(id=variants[0].id)
        sizes = Variant.objects.filter(product_id = variant.product_id).order_by('size__id').distinct('size__id')

    cart_product_form = CartAddProductForm()
    context = {'product': product,'cart_product_form': cart_product_form, 'sizes':sizes, 'colors':colors, 'query':query, 'variant':variant}
    return render(request,'detail.html',context)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variant.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
