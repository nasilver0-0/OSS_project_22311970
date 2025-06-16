from django.contrib import admin
from .models import Member, Ingredient, MealRecord, Settings

admin.site.register(Member)
admin.site.register(Ingredient)
admin.site.register(MealRecord)
admin.site.register(Settings)