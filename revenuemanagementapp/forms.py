from django import forms
from revenuemanagementapp.models import Expense, Income


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


class IncomeSearchingForm(forms.Form):
    RECEIVERS = [('', '-------')] + list(Income.objects.values_list('receiver', 'receiver').distinct())
    # ACCOUNTS = [
    #     ('', '------'),
    #     ('141', '141'),
    #     ('338', '338'),
    #     ('511', '511'),
    #     ('711', '711')
    # ]
    # account = forms.ChoiceField(choices=ACCOUNTS, label='Tài khoản', required=False)
    receiver = forms.ChoiceField(choices=RECEIVERS, label='Người nhận tiền', required=False)
