from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from django.shortcuts import redirect, get_object_or_404
from .models import Product 
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

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