from django.urls import path
from front import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.aboutus, name='aboutus'),
    path('courses/', views.courses, name='courses'),
    path('search/', views.search, name='search'),
    path('purchase/<int:course_id>/', views.purchase_course, name='purchase_course'),
    path('payment/success/', views.payment_success, name='payment_success'),  
    path('course_modules/<int:course_id>/modules/', views.course_modules, name='course_modules'),
    path('your-courses/', views.your_courses, name='your_courses'),
    path('all_courses/', views.all_courses, name='all_courses'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
