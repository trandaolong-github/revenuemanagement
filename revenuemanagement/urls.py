"""revenuemanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from revenuemanagementapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign-in/', auth_views.LoginView.as_view(template_name='sign_in.html'), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='/'), name='sign-out'),

    path('show-incomes/', views.show_incomes, name='show-incomes'),
    path('search-incomes/', views.income_search, name='search-incomes'),

    path('show-expenses/', views.show_expenses, name='show-expenses'),
    path('search-expenses/', views.expense_search, name='search-expenses'),

    path('search-incomes-expenses/', views.income_expense_search, name='search-incomes-expenses'),

    path('show-incomes-expenses/', views.show_incomes_expenses, name='show-incomes-expenses'),

    path('change-password/', views.change_password, name='change-password'),
    path('management/', views.management_home, name='management-home'),
    path('management/report/', views.management_report, name='management-report'),

    path('api/1/incomes/', views.IncomeList.as_view(), name="income-index"),
    path('api/1/incomes/<int:pk>/', views.IncomeDetail.as_view(), name="income-detail"),
    path('api/1/<str:_type>/info/', views.get_receivers_senders_addresses, name="info"),
    path('api/1/expenses/', views.ExpenseList.as_view(), name="expense-index"),
    path('api/1/expenses/<int:pk>/', views.ExpenseDetail.as_view(), name="expense-detail"),

    path('api/1/incomes-expenses/', views.get_incomes_expenses, name="income-expense-index"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
