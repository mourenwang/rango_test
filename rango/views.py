from datetime import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import *
from rango.froms import *
from rango.models import *
from django.http import *
from django.shortcuts import redirect

# Create your views here.


def index(request):
    """首页"""
    request.session.set_test_cookie()
    category_list = Category.objects.order_by("-likes")[:5]
    pases_list = Page.objects.order_by("-view")[:5]
    context_dict = {"categories": category_list, "pases": pases_list}
    # 调用处理 cookie 的辅助函数
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    """关于"""
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, "rango/about.html")


def show_category(request, category_name_slug):
    """查看分类"""
    context_dic = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-view')
        context_dic['pases'] = pages
        context_dic["category"] = category
    except Category.DoesNotExist:
        context_dic["pases"] = None
        context_dic["category"] = None
    return render(request, "rango/category.html", context_dic)


def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, "rango/add_category.html", {"form": form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                # probably better to use a redirect here.
            return show_category(request, category_name_slug, )
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict ,)


def register(request):
    registered = False
    user_form = UserForm()
    profile_form = UserProfileForm()
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' == request.FILES:
                profile.picture = request.FILES["picture"]
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    return render(request, "registration/registration_form.html", {"user_forn": user_form,
                                                   "profile_form": profile_form,
                                                   "registered": registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "registration/login.html", {})


"""def show_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("you're login")
    else:
        return HttpResponse("You are not logged in.")
"""


@login_required
def restricted(request):  # 限制登录
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # 可以确定用户已登录，因此直接退出
    logout(request)
    # 把用户带回首页
    return HttpResponseRedirect(reverse('rango:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):

    visits = int(request.COOKIES.get("visits",1))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                                '%Y-%m-%d %H:%M:%S')
    if (datetime.now()-last_visit_time).days>0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def track_url(request):
    page_id = None
    url = "/rango/"
    if request.method == "GET":
        if "page_id" in request.GET:
            page_id = request.GET["page_id"]
            try:
                page = Page.objects.get(id = page_id)
                page.view += 1
                page.save()
                url =page.url
            except:
                pass
    return redirect(url)

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('rango:index')
    else:
        print(form.errors)
    context_dict = {'form':form}
    return render(request, 'rango/profile_registration.html', context_dict)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return redirect("rango:index")
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
    else:
        print(form.errors)
    return render(request, 'rango/profile.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, "rango/list_profiles.html", {"userprofile_list": userprofile_list})


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
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

