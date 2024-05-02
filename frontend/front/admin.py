from django.contrib import admin
from .models import Course, Module, UserCourseAccess, Purchase, ScrapeCourse

class ModuleInline(admin.TabularInline):
    model = Module

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        ModuleInline,
    ]
    list_display = ('title', 'description', 'amount', 'num_modules')

admin.site.register(Course, CourseAdmin)
admin.site.register(Module)

class UserCourseAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')

admin.site.register(UserCourseAccess, UserCourseAccessAdmin)
admin.site.register(Purchase)

@admin.register(ScrapeCourse)
class ScrapeCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'amount', 'num_modules')