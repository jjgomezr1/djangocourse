from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from django.shortcuts import redirect, get_object_or_404
from .models import Product 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .utils import FileStorage
from pages.utils import ImageLocalStorage

# Create your views here.

class ImageViewNoDI(View):
  template_name = 'images/index.html'
  def get(self, request):
   image_url = request.session.get('image_url', '')

   return render(request, self.template_name, {'image_url': image_url})
  def post(self, request):
   image_storage = ImageLocalStorage()
   image_url = image_storage.store(request)
   request.session['image_url'] = image_url
   return redirect('image_index')

class UploadImageView(View):
    template_name = 'upload.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        storage = ImageLocalStorage()  # Sin abstracción
        image_url = storage.store(request)
        return render(request, self.template_name, {'image_url': image_url})

def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView

class UploadImageView(View):
    template_name = 'pages/upload.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        uploaded_file = request.FILES['image']  # Recibe el archivo
        storage = FileStorage()  # Usamos la clase de utils.py
        file_url = storage.save(uploaded_file, uploaded_file.name)
        return render(request, self.template_name, {'file_url': file_url})

class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Simulación de "base de datos"
        products = {
            121: {'name': 'Tv samsung', 'price': '1000'},
            11: {'name': 'Iphone', 'price': '2000'}
        }

        # Obtener productos del carrito desde sesión
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Datos para la vista
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Agregar un producto al carrito
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[str(product_id)] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')


class CartRemoveAllView(View):
    def post(self, request):
        # Vaciar el carrito
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')

class ProductForm(forms.ModelForm):
   class Meta: 
        model = Product 
        fields = ['name', 'price'] 

class ProductCreateView(View):
 template_name = 'products/create.html'
 def get(self, request):
  form = ProductForm()
  viewData = {}
  viewData["title"] = "Create product"
  viewData["form"] = form
  return render(request, self.template_name, viewData)
 def post(self, request):
  form = ProductForm(request.POST)
  if form.is_valid():
   form.save() 
   return redirect('index')
  else:
   viewData = {}
   viewData["title"] = "Create product"
   viewData["form"] = form
   return render(request, self.template_name, viewData)

class ProductListView(ListView): 
    model = Product 
    template_name = 'product_list.html' 
    context_object_name = 'products'  # This will allow you to loop through 'products' in your template 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Products - Online Store' 
        context['subtitle'] = 'List of products' 
        return context   

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all()
        }
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
 template_name = 'pages/about.html'

 def get_context_data(self, **kwargs):
  context = super().get_context_data(**kwargs)
  context.update({
   "title": "About us - Online Store",
   "subtitle": "About us",
   "description": "This is an about page ...",
   "author": "Developed by: Your Name",
  })
  return context
 
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact for our online store",
            "subtitle": "Contact us",
            "description": "You can contact us via email or phone.",
            "email": "soporte@example.com",
            "phone": "+57 000 000 0000"
        })
        return context