import matplotlib
matplotlib.use('Agg') # 맥 OS 스레드 충돌 해결 설정
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
from django.conf import settings

# -----------------------
# 1. 포지션 별 채용공고 
# -----------------------
def job_freq_hist(job_data):
    # 1. 한글 설정(macOS), json 파싱

    # font_path = ".ttf 파일 경로"
    # font_name = font_manager.FontProperties(fname=font_path).get_name()

    font_name = 'AppleGothic'
    plt.rc('font', family=font_name)

    # 2. {position: frequency} dict
    position_freq = {}

    for job in job_data:
        for pos in job.get('position', []):
            position_freq[pos] = position_freq.get(pos, 0) + 1

    # 3. position label 설정 (세로정렬)
    positions = []
    for pos in position_freq.keys():
        position = pos

        idx = pos.find('/')
        if idx != -1:
            position = pos[:idx + 1] + '\n' + pos[idx + 1:]

        idx = pos.find('(')
        if idx != -1:
            position = pos[:idx] + '\n' + pos[idx:]

        idx = pos.find(' ')
        if idx != -1:
            position = pos[:idx + 1] + '\n' + pos[idx + 1:]

        positions.append(position)

    # 4. plotting
    plt.figure(figsize=(30, 15))
    colors = ['red' if f >= 50 else 'green' for f in position_freq.values()]

    plt.bar(positions, position_freq.values(), width=0.75, color=colors)

    plt.title('포지션 별 채용 공고', fontsize=30)
    plt.xlabel('position', fontsize=20)
    plt.ylabel('frequency', fontsize=20)
    # plt.xticks(np.arange(0, len(position_freq.keys())), labels=positions, fontsize=13)
    ticks = np.arange(0, len(position_freq.keys())) # tick 오류 해결
    plt.xticks(ticks, labels=positions, fontsize=13)

    # 5. 이미지 저장 & 이미지 저장 경로 반환
    # 이미지 파일 이름
    img_path = 'data/images/'
    img_filename = 'job_frequency.png'
    img_file_path = img_path + img_filename

    # 이미지 저장
    plt.savefig(img_file_path)

    # 이미지 URL 생성
    img_url = img_file_path

    return img_url


# -----------------------
# 2.포지션 별 연관 기술 스택
# -----------------------
def job_tech_graph(job_data):  # job serializer
    # 1. 한글 설정 (macOS), json 파싱

    # font_path = ".ttf 파일 경로"
    # font_name = font_manager.FontProperties(fname=font_path).get_name()

    font_name = 'AppleGothic'
    plt.rc('font', family=font_name)

    # 2. position, tech_stack node
    position = set([])
    tech_stack = set([])
    for job in job_data:
        for pos in job.get('position', []):
            position.add(pos)
        for tech in job.get('tech_stack', []):
            tech_stack.add(tech)
    # print('---------position----------', position)
    # print('---------tech_stack----------', tech_stack)
    # 3. Graph node, edge 지정
    Bipart = nx.Graph()

    # position = ['시스템/네트워크', '서버/백엔드', '프론트엔드', '머신러닝'] # for testing
    Bipart.add_nodes_from(position, bipartite=0) # 그룹 1: position
    Bipart.add_nodes_from(tech_stack, bipartite=1) # 그룹 2: tech_stack

    edges = []
    for job in job_data:
        for pos in job.get('position', []):
            if pos in position:
                for tech in job.get('tech_stack', []):
                    edges.append((pos, tech))

    Bipart.add_edges_from(edges)

    # 4. tech_stack projection
    proj = bipartite.projected_graph(Bipart, tech_stack)
    pos = nx.spring_layout(proj)

    # 5. 차수 thresh 설정, thresh 이하의 노드는 표시 x
    degree = []
    print('--------nx.degree(proj)--------', degree)
    for node, deg in nx.degree(proj):
        degree.append(deg)

    degree = sorted(list(set(degree)))
    print('--------degree--------', degree)
    degree_thresh = degree[0]  # 차수 0인 노드는 제외 (최종 결과물_position 1개만 선택)
    max_degree = degree[-1]
    min_degree = degree[0]

    high_degree_node = []
    for node, deg in nx.degree(proj):
        degree.append(deg)
        if deg > degree_thresh:
            high_degree_node.append(node)

    proj_subnet = proj.subgraph(high_degree_node)

    # 6. 노드:차수 dict
    node_degrees = dict(proj_subnet.degree())
    node_sizes = {node: degree * 20 for node, degree in node_degrees.items()}  # 차수에 비례하는 크기 가짐
    node_values = {node: degree for node, degree in node_degrees.items()}  # 차수에 따른 색상 지정

    # 7. plotting
    cmap = plt.get_cmap('spring')
    plt.figure(figsize=(20, 15))
    plt.title('포지션 별 연관 기술 스택', fontsize=30)

    # subnet node, label, edge 지정
    nx.draw_networkx_nodes(proj_subnet, pos=pos, node_size=[node_sizes[n] for n in node_sizes.keys()],
                           node_color=list(node_values.values()),
                           cmap=cmap,
                           vmin=min_degree, vmax=max_degree)
    nx.draw_networkx_labels(proj_subnet, pos=pos, font_size=17, font_color='black')
    nx.draw_networkx_edges(proj_subnet, pos=pos, edge_color='lightgrey')

    # 8. 이미지 저장 & 이미지 저장 경로 반환
    # 이미지 파일 이름
    img_path = 'data/images/'
    img_filename = 'job_tech_hist.png'
    img_file_path = img_path + img_filename

    # 이미지 저장
    plt.savefig(img_file_path)

    # 이미지 URL 생성
    img_url = img_file_path

    return img_url

# -----------------------
# 3. 포지션 별 연봉 정보
# -----------------------
def wage_pos_hist(job_data):
    # 1. 한글 설정 (macOS), json 파싱

    # font_path = ".ttf 파일 경로"
    # font_name = font_manager.FontProperties(fname=font_path).get_name()

    font_name = 'AppleGothic'
    plt.rc('font', family=font_name)

    # 2. position: [min_sum, max_sum, 연봉 정보 기재된 job 개수] dict
    position_wage = {}
    anomaly = 500000000  # 5억 이상 -> 이상치 (~만원 기재정보 변환할 때 10000 더 곱해진듯)
    anomaly_div = 10000

    for job in job_data:
        for pos in job.get('position', []):
            min_wage = job.get("min_wage", -1)
            max_wage = job.get("max_wage", -1)
            if min_wage == -1 or max_wage == -1:
                continue

            if min_wage > anomaly:
                min_wage //= anomaly_div
            if max_wage > anomaly:
                max_wage //= anomaly_div

            position_wage[pos] = position_wage.get(pos, [])
            # 초기화
            if len(position_wage[pos]) == 0:
                position_wage[pos] = [min_wage, max_wage, 1]
            else:
                position_wage[pos][0] += min_wage
                position_wage[pos][1] += max_wage
                position_wage[pos][2] += 1

    # 평균 min, max
    for pos, wage in position_wage.items():
        position_wage[pos][0] = wage[0] // wage[2]
        position_wage[pos][1] = wage[1] // wage[2]

    # 3. position label 설정 (세로정렬)
    positions = []
    for pos in position_wage.keys():
        position = pos

        idx = pos.find('/')
        if idx != -1:
            position = pos[:idx + 1] + '\n' + pos[idx + 1:]

        idx = pos.find('(')
        if idx != -1:
            position = pos[:idx] + '\n' + pos[idx:]

        idx = pos.find(' ')
        if idx != -1:
            position = pos[:idx + 1] + '\n' + pos[idx + 1:]

        positions.append(position)

    # 4. plotting
    min_list = []
    max_list = []

    for wage in position_wage.values():
        min_list.append(wage[0])
        max_list.append(wage[1])

    plt.figure(figsize=(50, 15))

    index = np.arange(len(positions))
    bar_width = 0.25

    min_bar = plt.bar(index, min_list, bar_width, alpha=0.5, color='blue', label='min_wage')
    max_bar = plt.bar(index + bar_width, max_list, bar_width, alpha=0.5, color='red', label='max_wage')

    plt.title('포지션 별 연봉 정보', fontsize=50)
    plt.xlabel('position', fontsize=30)
    plt.ylabel('wage', fontsize=30)
    plt.xticks(np.arange(0, len(position_wage.keys())), labels=positions, fontsize=20)

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticks(current_values) # tick 오류 해결
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values], fontsize=20)


    # 5. 이미지 저장 & 이미지 저장 경로 반환
    img_path = 'data/images/'
    img_filename = 'job_wage_hist.png'
    img_file_path = img_path + img_filename

    # 이미지 저장
    plt.savefig(img_file_path)

    # 이미지 URL 생성
    img_url = img_file_path

    return img_url