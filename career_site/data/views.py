from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .serializers import JobSerializer, CompanySerializer
from .forms import *
from .models import *
from visualization.job_visualization import *
from visualization.company_visualization import *
import json


# Create your views here.
def index(request):
    return render(request, 'data/index.html')


def company(request):
    form = CompanyForm(request.POST or None)
    companies = None
    plots = {}
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            companies = Company.objects.filter(
                num_employees__gte=form.cleaned_data.get('num_employees'),
                investment__gte=form.cleaned_data.get('investment'),
                revenue__gte=form.cleaned_data.get('revenue')
            )

            company_data = CompanySerializer(companies, many=True).data
            plots['hist'] = visualize_company_employees(company_data)
            plots['bubble_map'] = visualize_company_location(company_data)
            plots['clustered_bubble_map'] = visualize_dong_location(company_data)
            print(plots)

    return render(request, 'data/company.html', {'form': form, 'companies': companies,
                                                 'plots': plots})


def job_search(request):
    form = JobSearchForm()
    return render(request, 'data/job.html', {'form': form})


def job_search_api(request):
    form = JobSearchForm(request.POST)
    if form.is_valid():
        positions = form.cleaned_data['position']
        min_experience = form.cleaned_data['min_experience']
        min_wage = form.cleaned_data['min_wage']

        job_position_mapping = JobPositionMapping.objects.filter(
            position_id__in=[position.id for position in positions]).select_related('job_id')

        jobs = Job.objects.filter(id__in=[mapping.job_id.id for mapping in job_position_mapping],
                                  min_wage__gte=min_wage,
                                  min_experience__gte=min_experience)

        job_serializer = JobSerializer(jobs, many=True)

        return JsonResponse({'data': job_serializer.data}, safe=False, json_dumps_params={'ensure_ascii': False})

        # JSON 파일로 디스크에 저장
        # serialized_data = job_serializer.data
        # with open('PATH/refined_job_api.json', 'w', encoding='utf-8') as f:
        #     json.dump(serialized_data, f, ensure_ascii=False, indent=4)

        # return JsonResponse(serialized_data, safe=False)


def create_img(request):
    if request.method == 'POST':
        job_data = json.loads(request.body)['data']

        # 각 시각화 함수를 호출하고 결과 이미지 파일의 경로를 저장
        job_freq_hist_path = job_freq_hist(job_data)
        job_tech_graph_path = job_tech_graph(job_data)
        wage_pos_hist_path = wage_pos_hist(job_data)

        # 결과 이미지 파일의 경로를 URL로 변환
        job_freq_hist_url = settings.STATIC_URL + job_freq_hist_path
        job_tech_graph_url = settings.STATIC_URL + job_tech_graph_path
        wage_pos_hist_url = settings.STATIC_URL + wage_pos_hist_path

        print(job_freq_hist_url)
        # 결과 이미지 파일의 경로를 JSON 형식으로 반환
        return JsonResponse({
            'job_freq_hist': job_freq_hist_url,
            'job_tech_graph': job_tech_graph_url,
            'wage_pos_hist': wage_pos_hist_url,
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
