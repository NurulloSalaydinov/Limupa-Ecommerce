from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View
from .models import Category, Tag, Brand, Color, Product, Banner, SubBanner, Review
from .forms import ReviewForm


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'single-product.html'
    
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#         context['related_products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)
#         context['reviews'] = Review.objects.filter(product=self.object)
#         return context


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

