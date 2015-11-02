from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category #Category model
from rango.models import Page #Page model
from rango.forms import CategoryForm
from rango.forms import PageForm

def index(request):

    category_list = Category.objects.order_by('-likes')[:10]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'boldmessage': "We're looking for One Piece"}
    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):

    #dict for template
    context_dict = {}

    try:
        #find the slug
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_slug'] = category_name_slug

        #retrieve pages
        pages = Page.objects.filter(category=category)

        #add to dict under pages
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)
        
def add_category(request):
    #http post
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            #save to db
            form.save(commit=True)

            #show homepage
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)










