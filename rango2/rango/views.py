from django.shortcuts import render
from rango.models import Category #CH7
from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm


def index(request):

    category_list = Category.objects.order_by('-likes')[:5] 
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages':page_list} 

    return render( request, 'rango/index.html', context_dict)

def about(request):

    context_dict = { 'boldmessage': "About page. Put together by Lovisa Sundin, 2092502s" }

    return render( request, 'rango/about.html', context_dict)
    
    #return HttpResponse("About page. This tutorial has been put together by Lovisa Sundin, 2092502s. <br/> <a href='/rango/'>Index</a>")

def category(request, category_name_slug):
    #Think of this as you passing a url-argment called category_name_slug

    context_dict={}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        #Basically, this is the view for any given category. We pass that into the
        #dictionary
        context_dict['category_name_slug'] = category.slug

        pages = Page.objects.filter( category=category )

        context_dict['pages'] = pages
        context_dict['category']=category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict) #Refer to template

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

       
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            #If there is a category, then don
            if cat:  #If category is valid in the first place?
                page = form.save(commit=False)
                page.category = cat #Set its category-field to that of cat-url
                page.views = 0  #Initialise views-field to 0
                page.save()     #Save the table
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'category_name_slug': category_name_slug} #Prepare context for template

    return render(request, 'rango/add_page.html', context_dict)
