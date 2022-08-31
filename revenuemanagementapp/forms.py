from django import forms
from revenuemanagementapp.models import Income, Expense


class CreateIncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('content', 'amount', 'account', 'income_type', 'accounting_voucher', 'budget', 'contract', 'branch', 'applicant', 'company', 'address')
        labels = {
            'content': "Nội dung thu tiền",
            'amount': "Số tiền",
            'account': "Tài khoản",
            'income_type': "Loại doanh thu",
            'accounting_voucher': "Chứng từ",
            'budget': "Mã ngân sách",
            'contract': "Mã hợp đồng/công trình",
            'branch': "Chi nhánh",
            'applicant': "Họ tên người nộp",
            'company': "Công ty",
            'address': "Địa chỉ"
        }


class CreateExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('content', 'amount', 'account', 'expense_type', 'accounting_voucher', 'budget', 'contract', 'branch', 'applicant', 'company', 'address')
        labels = {
            'content': "Nội dung chi tiền",
            'amount': "Số tiền",
            'account': "Tài khoản",
            'expense_type': "Loại chi phí",
            'accounting_voucher': "Chứng từ",
            'budget': "Mã ngân sách",
            'contract': "Mã hợp đồng/công trình",
            'branch': "Chi nhánh",
            'applicant': "Họ tên người nộp",
            'company': "Công ty",
            'address': "Địa chỉ"
        }
