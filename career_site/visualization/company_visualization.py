import re
import matplotlib.pyplot as plt
import json
import matplotlib.font_manager as fm

import pandas as pd
import folium
from folium.plugins import MarkerCluster
from sklearn.preprocessing import MinMaxScaler

# -----------------------
# 1. 회사별 사원수 barchart
# -----------------------
def visualize_company_employees(company_data):
    # company data 가져오기
    # 한글설정 (macOS)
    
    # font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    # font_name = fm.FontProperties(fname=font_path, size=10).get_name()
    
    font_name='AppleSDGothicNeo'
    plt.rc('font', family=font_name, size=12)

    # 회사 이름, 사원수 딕셔너리
    new_data = {item["name"]:item["num_employees"] for item in company_data}

    companies = list(new_data.keys())
    employees = list(new_data.values())

    # 회사 이름 세로 출력
    companies = ['\n'.join(list(name)) for name in companies]

    # plot
    plt.figure(figsize=(100, 10))

    # 사원수가 50명 이상이면 빨간색 막대
    colors = ['red' if x >=50 else 'green' for x in employees]

    plt.bar(companies, employees, color=colors)
    plt.xlabel('회사')
    plt.ylabel('사원 수')
    plt.title('회사별 사원 수')

    # 이미지 저장, 반환
    img_path='company_barchart.png'
    plt.savefig(img_path)
    
    return img_path
    
# -----------------------
# 2. 회사별 지역 좌표 bubble
# -----------------------
def visualize_company_location(company_data):
    # company data 가져오기

    # 회사 데이터 딕셔너리 생성
    company_loc = {item['id']: 
                    {'name':item['name'], 
                     'address':item['location']['address'], 
                     'geo_lat': item['location']['geo_lat'], 
                     'geo_alt': item['location']['geo_alt']} 
                    for item in company_data}

    # 회사 데이터 df변환
    df = pd.DataFrame.from_dict(company_loc, orient='index')

    # 회사 위치 표시
    # 서울 중심부
    map = folium.Map(location=[37.5665, 126.9780], zoom_start=10)

    # 회사 위치 버블 표시
    for idx, row in df.iterrows():
        folium.CircleMarker(location=[row['geo_lat'], row['geo_alt']],
                            popup=row['name'], # 팝업으로 회사 이름 표시
                            radius=2, # 노드 크기
                            fill=True,
                            color='red'
                            ).add_to(map)

    # 이미지 저장, 반환
    map_path=('map_company.html')
    map.save(map_path)
    
    return map_path

# -----------------------
# 3. 회사별 동 카운트 bubble
# -----------------------
def visualize_dong_location(company_data):
    
    # 필요한 데이터 딕셔너리 생성
    company_loc = {item['id']: 
                    {'name':item['name'], 
                     'address':item['location']['address'], 
                     'geo_lat': item['location']['geo_lat'], 
                     'geo_alt': item['location']['geo_alt']} 
                    for item in company_data}

    # 회사 데이터 df변환
    df = pd.DataFrame.from_dict(company_loc, orient='index')

    # df_dong 생성
    # 주소에서 '동' 추출
    df['dong'] = df['address'].apply(lambda x: re.search(r'\b[가-힣]*동\b', x).group() 
                                            if re.search(r'\b[가-힣]*동\b', x) else None)

    # 동별 개수 세기
    df_dong = df['dong'].value_counts().reset_index()

    df_dong.columns = ['dong', 'count']

    # 동 기준으로 위도와 경도의 평균 계산
    df_dong_mean = df.groupby('dong').agg({'geo_lat':'mean', 'geo_alt':'mean'}).reset_index()

    # df_dong + 동별 평균 좌표 컬럼
    # 동별 개수와 평균 위도, 경도를 결합
    df_final = pd.merge(df_dong, df_dong_mean, on='dong')
    map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # 동 별로 회사의 개수 표시
    # MarkerCluster 인스턴스 생성
    marker_cluster = MarkerCluster().add_to(map)

    # 맵에 회사 위치 추가
    for idx, row in df.iterrows():
        # 각 회사의 위도, 경도
        folium.CircleMarker(location=[row['geo_lat'], row['geo_alt']],
                            radius=1,
                            popup=row['name'],
                            fill=True,
                            color='red').add_to(map)

    for idx, row in df_final.iterrows():
        # 각 동의 위도, 경도
        folium.Marker(location=[row['geo_lat'], row['geo_alt']], 
                    radius=3,
                    popup=row['dong'],
                    color='black',
                    fill=True,
                    fill_color='black',
                    icon=folium.Icon(color='black', icon='star')
                    ).add_to(marker_cluster)

    # 이미지 저장, 반환
    map_path = 'map_dong.html'
    map.save(map_path)
    
    return map_path