from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime
from rango.bing_search import run_query

#main page
def index(request):

    category_list = Category.objects.all()
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request,'rango/index.html', context_dict)

    return response


#about
def about(request):
    
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict = {'boldmessage': "We're looking for One Piece", 'visits': count}
    return render(request, 'rango/about.html', context_dict)

#category
def category(request, category_name_slug):

    #dict for template
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None

    #check for POST request
    if request.method == 'POST':
        #removes whitespace?
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query
    try:
        #find the slug
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_slug'] = category_name_slug

        #retrieve pages
        pages = Page.objects.filter(category=category).order_by('-views')

        #add to dict under pages
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)
        
#add category
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

#add page
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

#bing search
def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

#track views from rango
#before the urls are directed to their destinary, they pass through this view
#this view is expecting a get request that will provide the id of the page that has been clicked
def track_url(request):
    #set defaults first
    page_id = None
    url = '/rango/'

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)

    
# Use the login_required() decorator to ensure only those logged in can access the view.
#for restriction
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html') 

#like category
#in the url query string, the name can be invoked by GET['key']
#view works when there is a GET request
@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)

#helper function to get category list
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    #query database
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    #if the cat list is too large, trim it down to max_results
    if max_results > 0:
        if cat_list.count() > max_results:
            cat_list = cat_list[:max_results]

    return cat_list

def suggest_category(request):

    cat_list = []
    starts_with = ''
    #process get request
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    #call helper function
    cat_list = get_category_list(8, starts_with)

    #reuse the template from template tags
    return render(request, 'rango/cats.html', {'cats': cat_list })









