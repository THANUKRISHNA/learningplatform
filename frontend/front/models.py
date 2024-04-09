from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    num_modules = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='course_images/', default='default.jpg')

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    order = models.PositiveIntegerField()
    video_url = models.URLField(blank=True)  
    notes = models.FileField(upload_to='module_notes/', blank=True)  

    def __str__(self):
        return self.title



class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
