from django import forms
from .models import Company, Job, Position


class CompanyForm(forms.ModelForm):
    num_employees = forms.IntegerField(required=False, min_value=0, label='사원 수', initial=0)
    investment = forms.IntegerField(required=False, min_value=0, label='투자 금액(원)', initial=0)
    revenue = forms.IntegerField(required=False, min_value=0, label='매출(원)', initial=0)
    get_json = forms.BooleanField(required=False, label='Json 응답 반환')

    class Meta:
        model = Company
        fields = ['num_employees', 'revenue', 'investment']


class JobSearchForm(forms.ModelForm):
    # position = forms.ModelChoiceField(queryset=Position.objects.all(), label='직무')
    position = forms.ModelMultipleChoiceField(queryset=Position.objects.all(),
                                              label='직무',
                                              widget=forms.CheckboxSelectMultiple)

    min_experience_choice = [(i, f"{i}년 이상") if i > 0 else (i, "신입") for i in range(10)]
    min_experience = forms.ChoiceField(choices=min_experience_choice, label='경력')

    min_wage_choice = [(i * 1000, f"{str(i)[0]},{str(i)[1:]} 이상") for i in range(3000, 8000 + 1, 500)]
    min_wage = forms.ChoiceField(choices=min_wage_choice, label='연봉')


    class Meta:
        model = Job
        fields = ['position', 'min_experience', 'min_wage']
