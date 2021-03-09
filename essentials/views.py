import json
import random
from django.shortcuts import render
from django.db.models import Q, Avg, Count
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.safestring import SafeString
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.core import serializers
from essentials.models import Color
from essentials.forms import SearchForm 
from cart.forms import CartAddProductForm
from .models import Category, Product, Variant, Design, Placement, Method
from account.mixins import SellerAccountMixin
from tasarimlar.models import Design as design_for_sale
from itertools import chain




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



def product_list(request, category_slug=None):
    category = None
    parent = None
    categories = Category.objects.filter(active=True)
    parent_categories = Category.objects.filter(active=True, parent=None) 

    products_list = Product.objects.filter(active=True).order_by('id').distinct('id')
    page = request.GET.get('page', 1)

    paginator = Paginator(products_list, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if category.parent:
            parent = category.parent
            products_list = Product.objects.filter(active=True, category=category).order_by('id').distinct('id')
            page = request.GET.get('page', 1)
            paginator = Paginator(products_list, 12)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
        else:
            products_list = Product.objects.filter(active=True, category=category).order_by('id').distinct('id')
            page = request.GET.get('page', 1)
            paginator = Paginator(products_list, 12)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
    return render(request,
                  'list.html',
                  {'category': category,
                   'categories': categories,
                   'parent':parent,
                   'parent_categories': parent_categories,
                   'products_list': products_list, #to calculate how many products are there in the category
                   'products': products})

@login_required(login_url='/signup/')
def product_detail(request, id, slug):
    #query = request.GET.get('q')
    product = get_object_or_404(Product,id=id,slug=slug,active=True)
    #techniques = product.technique.all()

    variants = Variant.objects.filter(product_id=id).order_by('color_id')
    variant = Variant.objects.get(id=variants[0].id)
    sizes = Variant.objects.filter(product_id = product.id).order_by('size_id').distinct('size__id')
    colors = Variant.objects.filter(product_id=id,size_id=variants[0].size_id ).order_by('color_id').distinct('color__id')

    others = list(Product.objects.all())
    if len(others) > 7:
        qty = 7
    else:
        qty = len(others)
    others = random.sample(others, qty)
    
    cart_product_form = CartAddProductForm()
    context = {'product': product,'cart_product_form': cart_product_form,'sizes':sizes, 'colors':colors,  'variant':variant, 'others':others}
    return render(request,'detail2.html',context)

def change_size(request):
    data = {}
    form = CartAddProductForm()
    #if request.POST.get('action') == 'post':
    if request.is_ajax:
        product_id = request.GET.get('product_id')
        size_id = request.GET.get('size')
        color_id = request.GET.get('color_id', None)
        product_type =  request.GET.get('type', None)
        #variant, placement ve size price'i degistirmek icin gerekli
        #variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0]
        try:
            variant = Variant.published.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        except:
            # eger size degistirildiginde secili renk o size'da yoksa ilk rengi sec
            variant = Variant.published.filter(product_id=product_id, size_id=size_id, color__texture__isnull=False).order_by('color_id')[0]

        if variant.color.texture:
            data['color_id'] = variant.color.texture.url
        else:
            data['color_id'] = variant.color.color_code 

        #color options
        colors = Variant.published.filter(product_id=product_id, size_id=size_id).order_by('color_id')
        context = {'size_id': size_id, 'colors': colors, 'variant':variant}
        if product_type == 'blank':
            place_id = request.GET.get('place_id', None)
            placement = get_object_or_404(Placement, id=place_id)
            data['price_all_included'] = variant.variant_price()+placement.placement_price()
            data['rendered_table'] =  render_to_string('blank_page_color_list.html', context=context, request=request)
        else:
            method_id = request.GET.get('method_id', None)
            method = get_object_or_404(Method, id=method_id)
            place_id = request.GET.get('place_id', None)
            placement = get_object_or_404(Placement, id=place_id)
            data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price()
            data['rendered_table'] =  render_to_string('color_list.html', context=context, request=request)
            
        context2 = {'ajax_variant':variant,'form':form}
        data['variant_add_to_cart_url'] = render_to_string('add_to_cart_form.html',context=context2, request=request)
        #"/cart/add/"+str(variant.id)+"/"
        
        return JsonResponse(data)
    return JsonResponse(data)

def change_place(request):
    data = {}
    if request.is_ajax:
        product_id = request.GET.get('product_id', None)
        size_id = request.GET.get('size_id', None)
        color_id = request.GET.get('color_id', None)
        product_type =  request.GET.get('type', None)
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        if product_type == 'blank':
            place_id = request.GET.get('place_id', None)
            placement = get_object_or_404(Placement, id=place_id)
            data['price_all_included'] = variant.variant_price()+placement.placement_price()
        else:
            method_id = request.GET.get('method_id', None)
            method = get_object_or_404(Method, id=method_id)
            place_id = request.GET.get('place_id', None)
            placement = get_object_or_404(Placement, id=place_id)
            data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price()
        data['ajax'] = 'true'
        return JsonResponse(data)
    data['ajax'] = 'false'
    data['price_all_included'] = 0
    return JsonResponse(data)

def change_method(request):
    data = {}
    if request.is_ajax:
        product_id = request.GET.get('product_id', None)
        size_id = request.GET.get('size_id', None)
        color_id = request.GET.get('color_id', None)
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        method_id = request.GET.get('method_id', None)
        if method_id != 'none':
            place_id = request.GET.get('place_id', None)
            placement = get_object_or_404(Placement, id=place_id)
            method = get_object_or_404(Method, id=method_id)
            data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price()
        else:
            data['price_all_included'] = variant.variant_price()
        return JsonResponse(data)


def change_color(request):
    data = {}
    form = CartAddProductForm()
    if request.is_ajax:
        product_id = request.GET.get('product_id', None)
        size_id = request.GET.get('size_id', None)
        color_id = request.GET.get('color_id', None)
        product_type =  request.GET.get('type', None)
        #variant, placement ve size price'i degistirmek icin gerekli
        color = get_object_or_404(Color, id=color_id)
        if color.texture:
            data['color_id'] = color.texture.url
        else:
            data['color_id'] = color.color_code
        print(product_id, color_id, size_id)
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        
        if product_type == 'blank':
            place_id = request.GET.get('place_id', None)
            placement = get_object_or_404(Placement, id=place_id)
            data['price_all_included'] = variant.variant_price()+placement.placement_price()
        else:
            method_id = request.GET.get('method_id', None)
            method = get_object_or_404(Method, id=method_id)
            place_id = request.GET.get('place_id', None)
            placement = get_object_or_404(Placement, id=place_id)
            data['price_all_included'] = variant.variant_price()+placement.placement_price()+method.method_price()
        

        context = {'ajax_variant':variant,'form':form}
        data['variant_add_to_cart_url'] = render_to_string('add_to_cart_form.html',context=context, request=request)
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
    form = CartAddProductForm(request.POST)
    if request.is_ajax:
        color_id = request.GET.get('color_id', None)
        size_id = request.GET.get('size_id', None)
        product_id = request.GET.get('product_id', None)

        #variant, placement ve size price'i degistirmek icin gerekli
        variant = Variant.objects.filter(product_id=product_id, color_id=color_id, size_id=size_id)[0] #burda get  de kullanabilirdim ama olaki size id'si ve color id'si ayni olan variant olusturulursa ilki secilecek
        data['variant_id'] = variant.id
        
        context = {'ajax_variant':variant,'form':form}
        data['variant_add_to_cart_url'] = render_to_string('add_to_cart_form.html',context=context, request=request)
        return JsonResponse(data)



def product_design(request):
    return render(request,'product_design.html')

@login_required(login_url='/signup/')
def blank_single_item(request, id, slug, parent_category=None, subcategory=None):
    query = request.GET.get('q')
    product = get_object_or_404(Product,id=id,slug=slug,active=True)
    category = None #urun hicbir kategoride degilse bunun olmasi gerekiyor

    if subcategory:
        category = get_object_or_404(Category, slug=subcategory)
    else:
        for i in product.category.all():
            # parenti olan ilk urunu al
            while i.parent:
                category = i
                break
                

    #bu yukarindakinden sonra gelmeli cunku else oldugunda category productini aliyor. category onceden belli olmasi lazim
    if parent_category:
        parent = get_object_or_404(Category, slug=parent_category)
    else:
        # eger kategorinin parenti yoksa parent None olmasi gerekiyor cunku category diye tanimladigimin kendisi parent
        #if category'yi eklemek zorundayim cunku urun hicbir kategoride degilse o olmadan hata veriyor
        if category and category.parent:
            parent = category.parent
        else:
            parent = None
        
    others = list(Product.objects.filter(active=True))
    if len(others) > 3:
        qty = 3
    else:
        qty = len(others)
    others = random.sample(others, qty)

    variants = Variant.published.filter(product_id=id).order_by('size__row_no','color_id',)
    variant = Variant.published.get(id=variants[0].id)
    sizes = Variant.published.filter(product_id = product.id).order_by('size_id').distinct('size__id')
    #sizes = product.szs.all()
    colors = Variant.published.filter(product_id=id,size_id=variants[0].size_id ).order_by('color_id').distinct('color__id')
    
    cart_product_form = CartAddProductForm()
    context = {'product': product,'cart_product_form': cart_product_form,'sizes':sizes, 'colors':colors,  'variant':variant, 'parent':parent,'category':category, 'others':others}
    return render(request,'blank-single-item.html',context)


def post_search(request):
    form = SearchForm()
    result_list = []
    query = request.POST.get('query')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        
        ).order_by('id')
        designs = design_for_sale.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        
        ).order_by('pk')
        result_list = list(chain(products, designs))
        
        context = {'form':form,'products':result_list}
        return render(request, 'search_page.html', context)

    context = {'form':form,'products':result_list}        
    return render(request, 'search_page.html', context)