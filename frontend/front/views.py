from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
import wikipedia
import requests
from datetime import datetime, timedelta
from front.models import Course, Purchase

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
    b={}
    if request.method=='GET':
        return render(request,'register.html')
    else:
        u=request.POST['uname']
        e=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        print(u,e,p)
        if(u==''or e==''or p==''or cp==''):
            b['err']="please fill the box"
            return render(request,'register.html',b)
        elif(p!=cp):
            b['err']="password not matched"
            return render(request,'register.html',b)
        else:
            if User.objects.filter(username=u).exists():
                b['err'] = "User with this username already exists"
                return render(request, 'register.html', b)
            else:
                user = User.objects.create_user(username=u, email=e, password=p)
                b['success']="registered successfully"
                return render(request,'register.html',b)
def user_logout(request):
    logout(request)
    return redirect(reverse('home'))
def aboutus(request):
    return render(request,'aboutus.html')
def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

#def search(request):
    search_results = None
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        search_results = wikipedia.search(search_query)
    return render(request, 'search.html', {'search_results': search_results})

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')

        
        wiki_search_results = search_wikipedia(search_query)

        if wiki_search_results is not None:
            
            search_results = []
            for result in wiki_search_results:
                title = result.get('title', '')
                summary = result.get('snippet', '')  
                url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"  
                search_results.append({'title': title, 'summary': summary, 'url': url})
            
            
            return render(request, 'search.html', {'search_results': search_results})
        else:
            
            return render(request, 'error.html', {'error_message': 'Error occurred during Wikipedia search'})
    else:
        
        return render(request, 'error.html', {'error_message': 'Invalid request method'})


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
        
        
        expiry_duration = timedelta(days=365)  
        purchase_date = datetime.now()
        expiry_date = purchase_date + expiry_duration

        
        purchase = Purchase.objects.create(user=user, course=course, purchase_date=purchase_date, expiry_date=expiry_date)

        
        return redirect('purchase_success')  
    else:
        pass


