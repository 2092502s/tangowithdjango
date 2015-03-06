from django.shortcuts import render
from rango.models import Category 
from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm, UserProfile
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import datetime
from rango.bing_search import run_query
from django.shortcuts import redirect

def track_url(request):
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

def profile(request):

    if not request.user.is_authenticated():
        return HttpResponse("Log in please")

    context_dict = {}
    user = request.user
    
    #Try to get existing information about user

    try:
        user_profile = UserProfile.objects.get( user = user )
        context_dict['user_profile'] = user_profile
    except:
        pass
    

    
    
    #We need to obtain username, e-mail, website, picture, put into context_dict
    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        #Basically, we wish to initialise the field
        form.fields('website').initial = user_profile.website
        context_dict['form'] = form
        
        context_dict['picture'] = usprofile.picture

        if form.is_valid():

            newp = form.save(commit=False)
            newp.user = request.user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            try:
                newp.save()
            except:
                user_profile.delete()
                newp.save()

            profile.save() 
            
        else:
            print profile_form.errors
    else:
        #display it 
        form = UserProfileForm()
        form.fields['website'].initial = user_profile.website
        context_dict['form'] = form
        context_dict['picture'] = user_profile.picture

    return render(request, 'registration/profile.html', context_dict)

def any_profile(request, user_name):

    context_dict = {}
    any_user = User.objects.get(username = user_name)
    #Get hold of user information

    #Try to get username and put it into dictionary
    try:
        user_profile = UserProfile.objects.get( user = any_name)
        context_dict['user_profile'] = user_profile
    except:
        return HttpResponse("This user does not seem to exist.")

    context_dict['user_name'] = user_name
    context_dict['any_user'] = any_user

    return render(request, 'registration/anyprofile.html', context_dict)

def all_users(request):
    all_users = User.objects.order_by('-username')
    context_dict = {'all_users' : all_users}
    return render(request, 'registration/all_users.html', context_dict)


def register_profile(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use only of UserProfileForm.
        profile_form = UserProfileForm(data=request.POST)

        # If the form is valid...
        if profile_form.is_valid():

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = request.user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'registration/profile_registration.html',
            {'profile_form': profile_form, 'registered': registered} )




def index(request):

	#Basically, this code is in three parts. One deals with lists and data.
	#One deals with visits. One deals with last visit.

	#Create a list of all objects within the class (i.e. table)
	#called Category and order them. Do similar for pages.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

	#Pass these into a context-dictionary
	#(which, I presume, is for the templates)
    context_dict = {'categories': category_list, 'pages': page_list}

	#Check whether the cookie you want exists on SERVER (??)
    visits = request.session.get('visits')
	
	#If it does not exist, let it be 1 (an integer already) WHYYY?
    if not visits:
        visits = 1
	
	#Do not reset last time
    reset_last_visit_time = False
	#See if there is a last_visit. If so, update it using datetime.
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
	
def search(request):

    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})


def about(request):

    
    #If it does not exist, let it be 1 (an integer already) WHYYY?

##    #Check whether the cookie you want exists on SERVER (??)
##    visits = request.session.get('visits')
##    if not visits:
##        visits = 1
##    	#Do not reset last time
##    reset_last_visit_time = False
##	#See if there is a last_visit. If so, update it using datetime.
##    last_visit = request.session.get('last_visit')
##    if last_visit:
##        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
##
##        if (datetime.now() - last_visit_time).seconds > 0:
##            # ...reassign the value of the cookie to +1 of what it was before...
##            visits = visits + 1
##            # ...and update the last visit cookie, too.
##            reset_last_visit_time = True
##    else:
##        # Cookie last_visit doesn't exist, so create it to the current date/time.
##        reset_last_visit_time = True
##
##    if reset_last_visit_time:
##        request.session['last_visit'] = str(datetime.now())
##        request.session['visits'] = visits
##    context_dict['visits'] = visits
##
##	
##
##        
# If the visits session varible exists, take it and use it.
# If it doesn't, we haven't visited the site so set the count to zero.
    
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict = { 'boldmessage': "About page. Put together by Lovisa Sundin, 2092502s", 'count' : count}
    

    return render( request, 'rango/about.html', context_dict)
    
    #return HttpResponse("About page. This tutorial has been put together by Lovisa Sundin, 2092502s. <br/> <a href='/rango/'>Index</a>")

@login_required
def category(request, category_name_slug):
    #Thin@login_requiredk of this as you passing a url-argment called category_name_slug
    context_dict={}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        #Basically, this is the view for any given category. We pass that into the
        #dictionary
        context_dict['category_name_slug'] = category.slug

        pages = Page.objects.filter( category=category ).order_by('-views')

        context_dict['pages'] = pages
        context_dict['category']=category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict) #Refer to template

@login_required
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

@login_required
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
	
##def register(request):
##
##
##    # Initialised boolean to control whether it was successful
##    registered = False
##
##    # If it's a HTTP POST, we're interested in processing form data.
##    if request.method == 'POST':
##        # Attempt to grab information from the raw form information.
##        # Note that we make use of both UserForm and UserProfileForm.
##        user_form = UserForm(data=request.POST)
##        profile_form = UserProfileForm(data=request.POST)
##
##        # If the two forms are valid...
##        if user_form.is_valid() and profile_form.is_valid():
##            # Save the user's form data to the database.
##            user = user_form.save()
##
##            # Now we hash the password with the set_password method.
##            # Once hashed, we can update the user object.
##            user.set_password(user.password)
##            user.save()
##
##            # Now sort out the UserProfile instance.
##            # Since we need to set the user attribute ourselves, we set commit=False.
##            # This delays saving the model until we're ready to avoid integrity problems.
##            profile = profile_form.save(commit=False)
##            profile.user = user
##
##            # Did the user provide a profile picture?
##            # If so, we need to get it from the input form and put it in the UserProfile model.
##            if 'picture' in request.FILES:
##                profile.picture = request.FILES['picture']
##
##            # Now we save the UserProfile model instance.
##            profile.save()
##
##            # Update our variable to tell the template registration was successful.
##            registered = True
##
##        # Invalid form or forms - mistakes or something else?
##        # Print problems to the terminal.
##        # They'll also be shown to the user.
##        else:
##            print user_form.errors, profile_form.errors
##
##    # Not a HTTP POST, so we render our form using two ModelForm instances.
##    # These forms will be blank, ready for user input.
##    else:
##        user_form = UserForm()
##        profile_form = UserProfileForm()
##
##    # Render the template depending on the context.
##    return render(request,
##            'rango/register.html',
##            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

##def user_login(request):
##
##    # If the request is a HTTP POST, try to pull out the relevant information.
##    if request.method == 'POST':
##        # Gather the username and password provided by the user.
##        # This information is obtained from the login form.
##        username = request.POST['username']
##        password = request.POST['password']
##
##        # Use Django's machinery to attempt to see if the username/password
##        # combination is valid - a User object is returned if it is.
##        user = authenticate(username=username, password=password)
##
##        # If we have a User object, the details are correct.
##        # If None (Python's way of representing the absence of a value), no user
##        # with matching credentials was found.
##		
##		
##        if user:
##            # Is the account active? It could have been disabled.
##            if user.is_active:
##                # If the account is valid and active, we can log the user in.
##                # We'll send the user back to the homepage.
##                login(request, user)
##                return HttpResponseRedirect('/rango/')
##            else:
##                # An inactive account was used - no logging in!
##                return HttpResponse("Your Rango account is disabled.")
##        else:
##            # Bad login details were provided. So we can't log the user in.
##			#Try to fetch a user from the database.
##			print "Invalid login details: {0}, {1}".format(username, password)
##			try:
##				maybeuser = User.objects.get( username=username )
##				return HttpResponse("Username exists, but password incorrect.")
##			except:
##				return HttpResponse("Username does not exist.")
##
##    # The request is not a HTTP POST, so display the login form.
##    # This scenario would most likely be a HTTP GET.
##    else:
##        # No context variables to pass to the template system, hence the
##        # blank dictionary object...
##        return render(request, 'rango/login.html', {})
##		
@login_required
def restricted(request):
	context_dict = {'boldmessage': "Since you're logged in, you can see this text!"}
	return render( request, 'rango/restricted.html', context_dict)

##@login_required
##def user_logout(request):
##	logout(request)
##	return HttpResponseRedirect('/rango/')
