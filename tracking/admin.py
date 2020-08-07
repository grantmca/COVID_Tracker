from django.contrib import admin

from .models import Case, Person, Test

# Register your models here.
admin.site.register(Case)
admin.site.register(Person)
admin.site.register(Test)