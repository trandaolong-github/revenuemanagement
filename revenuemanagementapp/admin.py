from django.contrib import admin

from revenuemanagementapp.models import Expense, Income

admin.site.register(Income)
admin.site.register(Expense)

# Register your models here.
