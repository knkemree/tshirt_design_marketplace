from django.shortcuts import render
from django.db.models import Q, Avg, Count
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from cart.forms import CartAddProductForm
from .models import Category, Product, Variant, Design, Placement, Method
from account.mixins import SellerAccountMixin
import json
from django.utils.safestring import SafeString
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.core import serializers
from essentials.models import Color



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
    categories = Category.objects.filter(active=True)
    parent_categories = Category.objects.filter(active=True, parent=None) 

    products = Product.objects.filter(active=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'list.html',
                  {'category': category,
                   'categories': categories,
                   'parent_categories': parent_categories,
                   'products': products})

def product_detail(request, id, slug):
    query = request.GET.get('q')
    product = get_object_or_404(Product,id=id,slug=slug,active=True)
    #techniques = product.technique.all()

    variants = Variant.objects.filter(product_id=id).order_by('color_id')
    variant = Variant.objects.get(id=variants[0].id)
    sizes = Variant.objects.filter(product_id = product.id).order_by('size_id').distinct('size__id')
    colors = Variant.objects.filter(product_id=id,size_id=variants[0].size_id ).order_by('color_id').distinct('color__id')
    #color = colors[0].color.name
    
    # if request.method == 'POST':
    #     variant_id = request.POST.get('variantid')                                                                                                                                                  
    #     variant = Variant.objects.get(id=variant_id) #selected product by click color radio
    #     sizes = Variant.objects.filter(product_id = variant.product_id).order_by('size_id').distinct('size__id') 
    #     colors = Variant.objects.filter(product_id=id,size_id=variant.size_id ).order_by('color_id').distinct('color__id')
    #     color = colors[0].color.name
    #     query += variant.product.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
    #     print(query)
    # else:
    #     variants = Variant.objects.filter(product_id=id).order_by('color_id')
    #     variant = Variant.objects.get(id=variants[0].id)
    #     sizes = Variant.objects.filter(product_id = variant.product_id).order_by('size_id').distinct('size__id')
    #     colors = Variant.objects.filter(product_id=id,size_id=variants[0].size_id ).order_by('color_id').distinct('color__id')
    #     color = colors[0].color.name
    
    cart_product_form = CartAddProductForm()
    context = {'product': product,'cart_product_form': cart_product_form,'sizes':sizes, 'colors':colors,  'variant':variant,}
    return render(request,'detail.html',context)

def change_size(request):
    data = {}
    #if request.POST.get('action') == 'post':
    if request.is_ajax:
        size_id = request.GET.get('size')
        product_id = request.GET.get('product_id')
        place_id = request.GET.get('place_id', None)
        method_id = request.GET.get('method_id', None)
        color_id = request.GET.get('color_id', None)

        placement = get_object_or_404(Placement, id=place_id)
        method = get_object_or_404(Method, id=method_id)
        

        #variant, placement ve size price'i degistirmek icin gerekli
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0]
        # try:
        #     variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        # except:
        #     # eger size degistirildiginde secili renk o size'da yoksa ilk rengi sec
        #     variant = Variant.objects.filter(product_id=product_id, size_id=size_id).order_by('color_id')[0]
        #     # .exclude(color_id__texture__isnull=True)
        #     print(variant.color)
        #     print('burayi print ediyor mu')

        
        if variant.color.texture:
            data['color_id'] = variant.color.texture.url
        else:
            data['color_id'] = variant.color.color_code    
        
        #color options
        colors = Variant.objects.filter(product_id=product_id, size_id=size_id).order_by('color_id')
        
        context = {'size_id': size_id, 'colors': colors, 'variant':variant,}

        data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price()
        data['rendered_table'] =  render_to_string('color_list.html', context=context, request=request)
        data['variant_add_to_cart_url'] = "/cart/add/"+str(variant.id)+"/"
        
        return JsonResponse(data)
    return JsonResponse(data)

def change_place(request):
    data = {}
    if request.is_ajax:
        product_id = request.GET.get('product_id', None)
        place_id = request.GET.get('place_id', None)
        method_id = request.GET.get('method_id', None)
        size_id = request.GET.get('size_id', None)
        color_id = request.GET.get('color_id', None)
        placement = get_object_or_404(Placement, id=place_id)
        method = get_object_or_404(Method, id=method_id)
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        
        print(placement, method, variant)
        data['ajax'] = 'true'
        data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price()
        return JsonResponse(data)
    data['ajax'] = 'false'
    data['price_all_included'] = 0
    return JsonResponse(data)

def change_method(request):
    data = {}
    if request.is_ajax:
        product_id = request.GET.get('product_id', None)
        place_id = request.GET.get('place_id', None)
        method_id = request.GET.get('method_id', None)
        size_id = request.GET.get('size_id', None)
        color_id = request.GET.get('color_id', None)
        placement = get_object_or_404(Placement, id=place_id)
        method = get_object_or_404(Method, id=method_id)
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        
        data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price()
        return JsonResponse(data)



def change_color(request):
    data = {}
    if request.is_ajax:
        product_id = request.GET.get('product_id', None)
        place_id = request.GET.get('place_id', None)
        method_id = request.GET.get('method_id', None)
        size_id = request.GET.get('size_id', None)
        color_id = request.GET.get('color_id', None)
        placement = get_object_or_404(Placement, id=place_id)
        method = get_object_or_404(Method, id=method_id)
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        
        

        #variant, placement ve size price'i degistirmek icin gerekli
        color = get_object_or_404(Color, id=color_id)
        if color.texture:
            data['color_id'] = color.texture.url
        else:
            data['color_id'] = color.color_code

        data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price(),
        data['variant_add_to_cart_url'] = "/cart/add/"+str(variant.id)+"/"
        return JsonResponse(data)
        #return render(request, 'product-gallery.html', context)
    return JsonResponse(data)


def dynamic_canvas(request):
    data = {}
    if request.is_ajax:
        product_id = request.GET.get('product_id', None)
        product = get_object_or_404(Product, id=product_id)
        placements = product.placements.all()
        for placement in placements:
            data[placement.id] = {}
            data[placement.id]['top'] = placement.top
            data[placement.id]['left'] = placement.left
            data[placement.id]['width'] = placement.width
            data[placement.id]['height'] = placement.height

            # data['width'] = str(placement)
        return JsonResponse(data)
    return JsonResponse(data)

def get_current_variant(request):
    data = {}
    if request.is_ajax:
        color_id = request.GET.get('color_id', None)
        size_id = request.GET.get('size_id', None)
        product_id = request.GET.get('product_id', None)

        #variant, placement ve size price'i degistirmek icin gerekli
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        data['variant_id'] = variant.id
        data['variant_add_to_cart_url'] = "/cart/add/"+str(variant.id)+"/"
        return JsonResponse(data)



def product_design(request):
    return render(request,'product_design.html')