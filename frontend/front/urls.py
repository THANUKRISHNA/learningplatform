from django.urls import path

from front import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.user_logout, name='logout'),
    path('about/',views.aboutus, name='aboutus'),
    path('courses/',views.courses, name='courses'),
    path('search/', views.search, name='search'),
    path('purchase/<int:course_id>/', views.purchase_course, name='purchase_course'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

