from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .serializers import JobSerializer, CompanySerializer
from .forms import *
from .models import *
from visualization.job_visualization import *
import json


# Create your views here.

def company(request):
    form = CompanyForm(request.POST or None)
    companies = None
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            companies = Company.objects.filter(
                num_employees__gte=form.cleaned_data.get('num_employees'),
                investment__gte=form.cleaned_data.get('investment'),
                revenue__gte=form.cleaned_data.get('revenue')
            )

            # 임시로 Json리턴하도록 설정
            if form.cleaned_data.get('get_json'):
                return JsonResponse(CompanySerializer(companies, many=True).data, safe=False,
                                    json_dumps_params={'ensure_ascii': False})

    return render(request, 'data/company.html', {'form': form, 'companies': companies})


def job_search(request):
    form = JobSearchForm()
    return render(request, 'data/job.html', {'form': form})


def job_search_api(request):
    form = JobSearchForm(request.POST)
    if form.is_valid():
        position = form.cleaned_data['position']
        min_experience = form.cleaned_data['min_experience']
        min_wage = form.cleaned_data['min_wage']

        target_position = get_object_or_404(Position, pk=position.id)
        job_position_mapping = JobPositionMapping.objects.filter(position_id=target_position.id)
        jobs = Job.objects.filter(id__in=[mapping.job_id.id for mapping in job_position_mapping],
                                  min_wage__gte=min_wage,
                                  min_experience__gte=min_experience)

        job_serializer = JobSerializer(jobs, many=True)
        # json_response = JsonResponse(job_serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})

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
        # job_tech_graph_path = job_tech_graph(job_data)
        wage_pos_hist_path = wage_pos_hist(job_data)

        # 결과 이미지 파일의 경로를 URL로 변환
        job_freq_hist_url = settings.MEDIA_URL + job_freq_hist_path
        # job_tech_graph_url = settings.MEDIA_URL + job_tech_graph_path
        wage_pos_hist_url = settings.MEDIA_URL + wage_pos_hist_path

        # 결과 이미지 파일의 경로를 JSON 형식으로 반환
        return JsonResponse({
            'job_freq_hist': job_freq_hist_url,
            # 'job_tech_graph': job_tech_graph_url,
            'wage_pos_hist': wage_pos_hist_url,
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
