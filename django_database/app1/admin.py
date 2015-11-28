from django.contrib import admin

# Register your models here.
from .models import faculty,teach,course

class teachinline(admin.StackedInline):
    model = teach
    extra=1

class facultyadmin(admin.ModelAdmin):
    inlines=[teachinline]
    list_display = ('fid', 'fname')

class courseadmin(admin.ModelAdmin):
    inlines=[teachinline]
    list_display = ('cid', 'cname')

admin.site.register(faculty,facultyadmin)
admin.site.register(teach)
admin.site.register(course,courseadmin)