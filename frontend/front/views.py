from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import wikipedia
import requests
from datetime import datetime, timedelta
from front.models import Course, Purchase, ScrapeCourse, UserCourseAccess, Module
from razorpay import Client
from django.conf import settings



def home(request):
    popular_courses = Course.objects.all()[:3]
    return render(request, 'home.html', {'popular_courses': popular_courses})


def user_login(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('uname')
        password = request.POST.get('upass')

        if not (username and password):
            context['err'] = "Please fill all the fields"
            return render(request, 'login.html', context)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
        else:
            context['err'] = "Incorrect username or password"
            return render(request, 'login.html', context)


def register(request):
    b = {}
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        u = request.POST['uname']
        e = request.POST['uemail']
        p = request.POST['upass']
        cp = request.POST['ucpass']
        print(u, e, p)
        if u == '' or e == '' or p == '' or cp == '':
            b['err'] = "please fill the box"
            return render(request, 'register.html', b)
        elif p != cp:
            b['err'] = "password not matched"
            return render(request, 'register.html', b)
        else:
            if User.objects.filter(username=u).exists():
                b['err'] = "User with this username already exists"
                return render(request, 'register.html', b)
            else:
                user = User.objects.create_user(
                    username=u, email=e, password=p)
                b['success'] = "registered successfully"
                return render(request, 'register.html', b)


def user_logout(request):
    logout(request)
    return redirect(reverse('home'))


def aboutus(request):
    return render(request, 'aboutus.html')


def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def search(request):
    search_results = None
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        search_results = wikipedia.search(search_query)
    return render(request, 'search.html', {'search_results': search_results})


def search_wikipedia(search_query):
    wiki_search_url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': search_query,
        'format': 'json'
    }
    try:
        response = requests.get(wiki_search_url, params=params)
        response.raise_for_status()
        search_results = response.json()['query']['search']
        return search_results
    except requests.RequestException as e:
        print("Error occurred:", e)
        return None


def purchase_course(request, course_id):
    if request.method == 'POST':
        user = request.user
        course = Course.objects.get(pk=course_id)
        amount = int(course.amount * 100)  

        razorpay_client = Client(auth=("rzp_test_47FqPXf9FYhJjr", "ydgcrbvgx09PGkdLt0hwtGto"))
        order = razorpay_client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        return render(request, 'payment.html', {'order': order, 'course': course, 'amount': amount})
    else:
        course_id = request.GET.get('course_id')  
        if course_id:
            course = Course.objects.get(pk=course_id)
            user = request.user
            expiry_duration = timedelta(days=365)
            purchase_date = datetime.now()
            expiry_date = purchase_date + expiry_duration
            purchase = Purchase.objects.create(user=user, course=course, purchase_date=purchase_date, expiry_date=expiry_date)
            return redirect('purchase_success')
        else:
            return redirect('home')


def payment_success(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
        user = request.user
        expiry_duration = timedelta(days=365)
        purchase_date = datetime.now()
        expiry_date = purchase_date + expiry_duration
        purchase = Purchase.objects.create(user=user, course=course,
                                            purchase_date=purchase_date, expiry_date=expiry_date)

        
        UserCourseAccess.objects.create(user=user, course=course)

        return redirect('purchase_success')
    else:
        return redirect('home')


def course_modules(request, course_id):
    course = Course.objects.get(pk=course_id)
    user = request.user

   
    if not UserCourseAccess.objects.filter(user=user, course=course).exists():
        return redirect('home')  

    modules = Module.objects.filter(course=course).order_by('order')
    return render(request, 'course_modules.html', {'course': course, 'modules': modules})


def your_courses(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user)
        print("Number of purchases:", purchases.count())  
        print("Purchases:", purchases)  
        return render(request, 'your_courses.html', {'purchases': purchases})
    else:
        return redirect('login')



def all_courses(request):
    courses = ScrapeCourse.objects.all()
    return render(request, 'all_courses.html', {'courses': courses})

def searchnav(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.none()
    return render(request, 'search_results.html', {'courses': courses, 'query': query})

def quiz(request):
    url = 'https://opentdb.com/api.php?amount=10&type=multiple'
    response = requests.get(url)
    quiz_data = response.json()
    questions = quiz_data['results']
    return render(request, 'quiz.html', {'questions': questions})

