from django.shortcuts import render,redirect,get_object_or_404
from . models import register_tbl,Book_tbl,ReadBook_tbl,ReadingList,SubscriptionPlan, UserSubscription,Payment,UserBook
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,"index.html")

def register(request):
    if request.method=="POST":
        nme=request.POST.get('fnm')
        lnm=request.POST.get('lnm')
        eml=request.POST.get('eml')
        psw=request.POST.get('npsd')
        # typ=request.POST.get('typ')
        obj=register_tbl.objects.create(fname=nme,lname=lnm,email=eml,password=psw)
        obj.save()
        if obj:
            return render(request,"login.html")
        else:
            return render(request,"register.html")
    return render(request,"register.html")

def login(request):
    if request.method=="POST":
        eml=request.POST.get('u')
        psw=request.POST.get('p')
       
        obj = register_tbl.objects.filter(email=eml,password=psw)
        if obj:
            
            user = obj.first()

            for i in obj:
                idno=i.id 
            request.session['idl']=idno

            request.session['ema']=eml
            request.session['psa']=psw
            request.session['type']=user.type

            if request.session.get('type')=='admin':
                return render(request,"admin/adminHome.html")
            # elif request.session.get('type')=='manager':
            #     return render(request,"manager/managerHome.html")
            
            else: 
                return render(request,"user/userHome.html")
            
        else:
                msg="Invalid Credentails!"
                return render(request,"login.html",{"error":msg})
    else:
        return render(request,"login.html")
  
def users(request):
    obj=register_tbl.objects.all()
    return render(request,"admin/users.html",{"data":obj})

def edit(req):
    idl=req.GET.get('idn')
    obj = register_tbl.objects.filter(id=idl)
    if req.method=="POST":
        fnm=req.POST.get('fn')
        idn=req.POST.get('idno')
        lnm=req.POST.get('ln')
        eml=req.POST.get('em')
        psd=req.POST.get('ps')
        obj =register_tbl.objects.filter(id=idn)
        obj.update(fname=fnm,lname=lnm,email=eml,password=psd)
        return redirect('/users')
    return render(req,"admin/editUser.html",{"data":obj})

def delete(request):
    idl=request.GET.get('idn')
    obj=register_tbl.objects.filter(id=idl)
    obj.delete()
    return redirect("/users")

def addbook(request):
    if request.method=='POST':
        bkt=request.POST.get('tle')
        bka=request.POST.get('aut')
        bkd=request.POST.get('des')
        bkc=request.POST.get('cat')
        bkimg=request.FILES.get('coimg')
        bk=request.FILES.get('pdf')
        obj=Book_tbl.objects.create(title=bkt,author=bka,description=bkd,cover_image=bkimg,pdf_file=bk,category=bkc)
        obj.save()
        if obj:
            msg="details added successfully!!"
            return render(request,"admin/addbooks.html",{"book":msg})
    return render(request,"admin/addbooks.html")

def viewbook(request):
    obj = Book_tbl.objects.all()
    return render(request,"admin/viewbooks.html",{"books":obj})

def delete_book(request, idl):
    Book_tbl.objects.filter(id=idl).delete()
    return redirect("/adminHome")

def userview(request):
    obj = Book_tbl.objects.all()
    return render(request,"user/userview.html",{"books":obj})

def readbook(request,book_id):
    bobj = Book_tbl.objects.get(id=book_id)
    obj = ReadBook_tbl.objects.filter(book=bobj)
    return render(request,"user/readbook.html",{"book":obj})


def search_books(request):
    keywords = request.GET.get('keywords', '').strip()
    catalog = request.GET.get('catalog', '')  # Can be 'Title' or 'Author'
    category = request.GET.get('category', '')

    books = Book_tbl.objects.all()

    # Filter by catalog (Title or Author)
    if catalog == "Title" and keywords:
        books = books.filter(title__icontains=keywords)
    elif catalog == "Author" and keywords:
        books = books.filter(author__icontains=keywords)

    # Filter by category if provided
    if category and category.lower() !="all":
        books = books.filter(category__iexact=category)

    return render(request, "user/searchbooks.html", {"books": books})

def login_view(request):
    if request.method=="POST":
        eml=request.POST.get('u')
        psw=request.POST.get('p')
       
        obj = register_tbl.objects.filter(email=eml,password=psw)
        if obj:
            
            user = obj.first()

            for i in obj:
                idno=i.id 
            request.session['idl']=idno

            request.session['ema']=eml
            request.session['psa']=psw
            request.session['type']=user.type

            if request.session.get('type')=='admin':
                return render(request,"admin/adminHome.html")
            
            
            else: 
                return render(request,"user/userHome.html")
            
        else:
                msg="Invalid Credentails!"
                return render(request,"login1.html",{"error":msg})
    return render(request,"login1.html")

def userHome(request):
    return render(request,"user/userHome.html")

def adminHome(request):
    return render(request,"admin/adminHome.html")

def admin_profile(request):
    if request.session.get('type') == 'admin':
        admin_id = request.session.get('idl')
        try:
            admin_obj = register_tbl.objects.get(id=admin_id)
            return render(request, "admin/profile.html", {"admin": admin_obj})
        except register_tbl.DoesNotExist:
            return redirect("login")  # If somehow not found
    else:
        return redirect("login")  # Block normal users
    
def edit_admin_profile(request):
    admin_id = request.session.get("idl")  # logged-in admin id
    admin = get_object_or_404(register_tbl, id=admin_id)

    if request.method == "POST":
        admin.fname = request.POST.get("name")
        admin.email = request.POST.get("email")
        admin.password = request.POST.get("password")
       

        if "profile_image" in request.FILES:
            admin.profile_image = request.FILES["profile_image"]

        admin.save()
        return redirect("admin_profile")  # redirect to profile after saving

    return render(request, "admin/editProfile.html", {"admin": admin})

def contact(request):
    return render(request,"contact.html") 

def collections(request):
    books = Book_tbl.objects.all()
    return render(request, "collections.html", {"books": books})

# Helper: check if user is admin
# def is_admin(user):
#     return user.is_staff or user.is_superuser

# @login_required
# @user_passes_test(is_admin)
def manage_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, "admin/manage_plans.html", {"plans": plans})

# @login_required
# @user_passes_test(is_admin)
def add_plan(request):
    if request.method == "POST":
        SubscriptionPlan.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            duration_days=request.POST.get("duration_days"),
            features=request.POST.get("features"),
            is_active=True if request.POST.get("is_active") == "on" else False
        )
        return redirect("manage_plans")
    return render(request, "admin/add_plan.html")

# @login_required
# @user_passes_test(is_admin)
def edit_plan(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    if request.method == "POST":
        plan.name = request.POST.get("name")
        plan.description = request.POST.get("description")
        plan.price = request.POST.get("price")
        plan.duration_days = request.POST.get("duration_days")
        plan.features = request.POST.get("features")
        plan.is_active = True if request.POST.get("is_active") == "on" else False
        plan.save()
        return redirect("manage_plans")
    return render(request, "admin/edit_plan.html", {"plan": plan})

# @login_required
# @user_passes_test(is_admin)
def delete_plan(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    plan.delete()
    return redirect("manage_plans")

def new_arrivals(request,):
    books = Book_tbl.objects.all()
    return render(request,"new_arrivals.html", {"books": books})

def trending(request):
    books = Book_tbl.objects.all()
    trending_books = Book_tbl.objects.filter(trending=True)  # only trending
    return render(request, "trending.html", {
        "books": books,
        "trending_books": trending_books
    })

def admin_view_collections(request):
    books = Book_tbl.objects.all()
    return render(request, "admin/adm_tmp_collections.html", {"books": books})



# Show all books
def book_lists(request):
    books = Book_tbl.objects.all()
    return render(request, "bookList.html", {"books": books})

def my_reading_list(request):
    if 'idl' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    uid = request.session['idl']
    user = get_object_or_404(register_tbl, id=uid)

    reading_list = ReadingList.objects.filter(user=user)  # ✅ filter by user

    return render(request, "my_reading_lists.html", {"reading_list": reading_list})


@login_required
def read_book(request, book_id):
    book = get_object_or_404(Book_tbl, id=book_id)
    return render(request, "user/readBook.html", {"book": book})


######################################

def add_to_reading_list(request, idn):
    if "idl" not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    book = get_object_or_404(Book_tbl, id=idn)
    uid = request.session["idl"]
    user = get_object_or_404(register_tbl, id=uid)

    # ✅ Check subscription status
    subscription = UserSubscription.objects.filter(
        user=user, is_active=True, end_date__gte=timezone.now()
    ).first()

    if not subscription:  # No active plan
        messages.warning(request, "Only subscribed users can create a reading list.")
        return redirect("available_books")

    # ✅ Check if already in reading list
    if ReadingList.objects.filter(book=book, user=user).exists():
        messages.info(request, "This book is already in your list.")
    else:
        ReadingList.objects.create(book=book, user=user)
        messages.success(request, f"{book.title} added to your reading list.")

    return redirect("/my_reading_list")


def remove_from_reading_list(request, book_id):
    if 'idl' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    uid = request.session['idl']
    # Find the book and user
    book = get_object_or_404(Book_tbl, id=book_id)
    user = get_object_or_404(register_tbl, id=uid)

    # Find the reading list item
    item = ReadingList.objects.filter(book=book, user=user).first()
    if item:
        item.delete()
        messages.success(request, f"{book.title} has been removed from your reading list.")
    else:
        messages.warning(request, "This book was not in your list.")

    return redirect("my_reading_list")


def user_profile(request):
    if 'idl' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    uid = request.session['idl']
    user = get_object_or_404(register_tbl, id=uid)

    # Get reading list count (optional)
    reading_list_count = ReadingList.objects.filter(user=user).count()

    return render(request, "profile.html", {
        "user": user,
        "reading_list_count": reading_list_count
    })

# def view_plans(request):
#     plans = SubscriptionPlan.objects.filter(is_active=True)
#     return render(request, "user/view_plans.html", {"plans": plans})

def my_subscription(request):
    if 'idl' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    uid = request.session['idl']
    user = get_object_or_404(register_tbl, id=uid)

    subscription = UserSubscription.objects.filter(user=user, is_active=True).first()
    return render(request, "user/my_subscription.html", {"subscription": subscription})

def subscribe(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    uid = request.session["idl"]  # same logic as reading list
    user = register_tbl.objects.get(id=uid)

    if request.method == "POST":
        # ✅ Step 1: Create a Payment record
        payment = Payment.objects.create(
            user=user,
            plan=plan,
            amount=plan.price,
            status="completed",  # mock as success
        )

        # ✅ Step 2: Activate subscription
        end_date = timezone.now() + timedelta(days=plan.duration_days)
        UserSubscription.objects.update_or_create(
            user=user,
            defaults={
                "plan": plan,
                "start_date": timezone.now(),
                "end_date": end_date,
                "is_active": True,
            },
        )

        # ✅ Step 3: Mark user as subscribed
        user.type = "subscribed"
        user.save()

        return redirect("my_subscription")

    # GET → show credit card form
    return render(request, "credit_card.html", {"plan": plan})

FREE_LIMIT = 3  # change to 5 if you want 5

def book_list(request):
    uid = request.session.get("idl")
    user = None
    if uid:
        try:
            user = register_tbl.objects.get(id=uid)
        except register_tbl.DoesNotExist:
            user = None

    now = timezone.now()
    # compute subscription status here (robust)
    is_subscribed = False
    if user:
        is_subscribed = UserSubscription.objects.filter(
            user=user, is_active=True, end_date__gt=now
        ).exists()

    books = Book_tbl.objects.all()
    allowed_books = books if is_subscribed else books[:FREE_LIMIT]

    # DEBUG: terminal output for quick diagnostics
    print(f"[DEBUG book_list] uid={uid} user_id={getattr(user,'id',None)} is_subscribed={is_subscribed} "
          f"total_books={books.count()} allowed_shown={allowed_books.count() if hasattr(allowed_books,'count') else len(allowed_books)}")

    return render(request, "books.html", {
        "books": allowed_books,
        "total_books": books.count(),
        "is_subscribed": is_subscribed,
    })

def access_book(request, book_id):
    if 'idl' not in request.session:  # ✅ check session
        messages.error(request, "Please log in first.")
        return redirect("login")

    uid = request.session['idl']
    user = get_object_or_404(register_tbl, id=uid)
    book = get_object_or_404(Book_tbl, id=book_id)

    # ✅ Check active subscription
    has_active_sub = UserSubscription.objects.filter(
        user=user, is_active=True, end_date__gt=timezone.now()
    ).exists()

    if has_active_sub:
        # subscribed → allow unlimited access
        UserBook.objects.get_or_create(user=user, book=book)
        return render(request, "book_detail.html", {"book": book})

    # ✅ Free user → check limit
    accessed_count = UserBook.objects.filter(user=user).count()
    if accessed_count < 5:
        UserBook.objects.get_or_create(user=user, book=book)
        return render(request, "book_detail.html", {"book": book})
    else:
        # hit free limit
        return render(request, "upgrade_message.html", {
            "message": "Free users can only read 5 books. Please subscribe for unlimited access!"
        })


def mybooks(request):
    books = Book_tbl.objects.all()
    return render(request, "mybooks.html", {"books": books})

def available_books(request):
    books = Book_tbl.objects.all()
    uid = request.session.get("idl")
    current_user = register_tbl.objects.get(id=uid)
    return render(request, "mybooks.html", {"books": books, "current_user": current_user})


# views.py
def admin_subscriptions(request):
    subs = UserSubscription.objects.select_related("user", "plan").all()
    return render(request, "admin/admin_subscriptions.html", {"subs": subs})

def delete_subscription(request, sub_id):
    sub = get_object_or_404(UserSubscription, id=sub_id)

    # ✅ When deleting, also mark the user as "user" again
    user = sub.user
    user.type = "user"
    user.save()

    sub.delete()
    return redirect("admin_subscriptions")

def view_plans(request):
    if "idl" not in request.session:
        return redirect("login")

    uid = request.session["idl"]
    user = register_tbl.objects.get(id=uid)

    # 🔍 Fetch active subscription for this user (not expired & active)
    subscription = (
        UserSubscription.objects.filter(user=user, is_active=True, end_date__gte=timezone.now())
        .order_by("-end_date")
        .first()
    )

    plans = SubscriptionPlan.objects.filter(is_active=True)

    return render(request, "user/view_plans.html", {
        "plans": plans,
        "subscription": subscription,   # ✅ pass to template
    })

def recommend_books(request):
    # 🔒 Check if user logged in
    if "idl" not in request.session:
        messages.error(request, "Please log in first to get recommendations.")
        return redirect("login")

    uid = request.session["idl"]
    user = register_tbl.objects.get(id=uid)

    # ✅ Block free users (only subscribed can use)
    subscription = UserSubscription.objects.filter(
        user=user, is_active=True, end_date__gte=timezone.now()
    ).first()

    if not subscription:
        messages.warning(request, "Only subscribed users can access recommendations.")
        return redirect("view_plans")

    recommendations = []

    if request.method == "POST":
        fav_genre = request.POST.get("genre", "").strip().lower()
        fav_author = request.POST.get("author", "").strip().lower()

        # Get all books from DB
        books = Book_tbl.objects.all()

        # Filter books by genre or author
        for book in books:
            if fav_genre in book.category.lower() or fav_author in book.author.lower():
                recommendations.append(book)

    return render(request, "user/recommend.html", {
        "recommendations": recommendations
    })

def edit_profile(request):
    if "idl" not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    uid = request.session["idl"]
    user = get_object_or_404(register_tbl, id=uid)

    if request.method == "POST":
        user.fname = request.POST.get("fname")
        user.lname = request.POST.get("lname")
        user.email = request.POST.get("email")

        if "profile_pic" in request.FILES:
            user.profile_pic = request.FILES["profile_pic"]

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")  # Redirect back to profile page

    return render(request, "edit_profile.html", {"user": user})

def media(request):
    return render(request,"media.html")