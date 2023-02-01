from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.db.models import Max, Min, Avg, Count, Q
from .models import Category, Tag, Brand, Color, Product, Banner, SubBanner, Review
from .forms import ReviewForm

# Max modeldagi fieldi maksimum qiymatini integer qaytaradi
# Min modeldagi fieldi minimum qiymatini integer qaytaradi
# Avg > Average modeldagi fieldi ortacha qiymatini integer qaytaradi
# Count modeldagi elementlar sonini qaytaradi

# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'single-product.html'
    
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#         context['related_products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)
#         context['reviews'] = Review.objects.filter(product=self.object)
#         return context

class ProductListView(ListView):
    queryset = Product.objects.order_by('-id')
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        request = self.request
        brands = request.GET.getlist('brand')
        categories = request.GET.getlist('category')
        sort = request.GET.get('sort')
        q = request.GET.get('q')
        # print(brands)
        # print(categories)
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
            # queryset = queryset.filter(title__icontains=q,description__icontains=q)
        if sort == '-cost':
            queryset = queryset.annotate(accurate_cost=( Max('cost') * ( 100 - Max('discount') ) / 100 )).order_by('-accurate_cost')
        elif sort == 'cost':
            queryset = queryset.annotate(accurate_cost=( Max('cost') * ( 100 - Max('discount') ) / 100 )).order_by('accurate_cost')
        if brands:
            queryset = queryset.filter(brand__id__in=brands)
        if categories:
            queryset = queryset.filter(category__id__in=categories)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['colors'] = Color.objects.all()
        context['tags'] = Tag.objects.all()
        return context

    


def product_detail_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    reviews = Review.objects.filter(product=product)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            rating = f.rating
            f.product = product
            f.save()
            product.rating_count += rating
            product.save()
            return redirect(request.path)
    context = {
        'object': product,
        'related_products': related_products,
        'reviews': reviews
    }
    return render(request, 'single-product.html', context)


def create_review(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    to = request.GET.get('to', '/')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.product = product
            f.save()
            return redirect(to)
    return redirect('/')


def home_view(request):
    categories = Category.objects.all()
    banners = Banner.objects.all()
    products = Product.objects.filter(category__slug='smart-phones')
    trendings = Product.objects.order_by('-id')
    sub_banners = SubBanner.objects.order_by('-id')[:3]
    context = {
        'categories': categories,
        'banners': banners,
        'sub_banners': sub_banners,
        'products': products,
        'trendings': trendings
    }
    return render(request, 'index.html', context)

