from django.contrib import admin
from .models import Course, Module

class ModuleInline(admin.TabularInline):
    model = Module

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        ModuleInline,
    ]
    list_display = ('title', 'description', 'amount', 'num_modules')

admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
