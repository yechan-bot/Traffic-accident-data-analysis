import io

import pymysql
import pandas as pd
import numpy as np
import folium
import seaborn as sns
from folium.plugins import MarkerCluster
from flask import Flask, request, render_template, redirect

def getConnection():
    return pymysql.connect(host = "127.0.0.1", port=3306, user='root', password='rudcjf2738!',
                           use_unicode=True, db='children_db', autocommit=True)


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.db import connection
from django.db.models.query import RawQuerySet
from django.views.generic.base import TemplateView
from matplotlib.backends.backend_agg import FigureCanvasAgg
from networkx.drawing.tests.test_pylab import plt
from django.db.models import Count, Sum
import matplotlib.pyplot as plt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from matplotlib import font_manager,rc
font_info='c:/Windows/Fonts/malgun.ttf'
font_name=font_manager.FontProperties(fname=font_info).get_name()
rc('font',family=font_name)



class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs): #오버라이딩 (데이터 추가할 것을 매개변수로 전달함)
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

from visual.models import list

def list_view(request):
    lists = list.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(lists, 20)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    context = {'lists': lines}
    return render(request, 'index.html', context)

def show_pandas(request):
        # 테스트용
        # test = list.objects.values('발생년').annotate(Count('발생년'))
        # print(test)
        # lists = test

        lists = list.objects.values('발생년').annotate(Count('발생년'))

        return render(request, 'year.html', {"lists": lists})
#    return render(request, 'year.html')


def show_map(request):
    return render(request, 'amap.html')

def show_time(request):
    fig = plt.figure()
    ax = fig.add_subplot(121)
    data = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data = pd.DataFrame(data)

    dt_jy = data.groupby('주야')
    dtjy = dt_jy['발생년'].count()

    labels1 = ['야', '주']

    ax = dtjy.plot(kind='pie', title='사고유형', figsize=(18, 6), fontsize=17, autopct='%.1f%%')

    ax = fig.add_subplot(122)
    data_df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data = pd.DataFrame(data_df)

    data["발생시"].unique()
    data_si = data["발생시"].value_counts()
    data_si.shape[0]
    for i in range(data_si.shape[0]):
        si = sns.countplot(data=data, x="발생시")
    for i in range(data_si.shape[0]):
        si.text(x=i, y=data_si[i], s=data_si[i], horizontalalignment='center')

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response

def show_chart(request):
    lists = list.objects.values('발생시').annotate(Count('발생시')).order_by('-발생시__count')

    return render(request, 'time.html', {"lists": lists})
#    return render(request, 'time.html')

def all_map(request):
    data = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv", encoding='utf-8')

    list1 = []
    list2 = []
    map = folium.Map([36.5427, 126.9168], zoom_start=10)
    chung = data[data['발생지시도'].str.contains('충남')]
    chung_location = chung[['발생지시도', '위도', '경도']]
    marker_cluster = MarkerCluster().add_to(map)

    for a in chung_location.index:
        folium.Marker(location=[chung_location.loc[a, "위도"], chung_location.loc[a, "경도"]],
                      zoom_start=12,
                      popup=chung_location.loc[a, "발생지시도"]).add_to(marker_cluster)
        list1.append(chung_location.loc[a, "위도"])
        list2.append(chung_location.loc[a, "경도"])
    amap_html = map.get_root().render()

    context = {'amap_html': amap_html}
    return render(request, 'amap.html', context)


def chart_hap(request):
    fig = plt.figure()
    ax = fig.add_subplot(122)
    data_df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data_df = pd.DataFrame(data_df)

    selectdata3 = data_df.groupby('발생년')
    selectdata4 = selectdata3['발생년'].count()

    labels2 = ['2015', '2016', '2017', '2018', '2019']
    ax = selectdata4.plot(kind='pie', title='사고유형', figsize=(18, 6), fontsize=17, autopct='%.1f%%')

    ax = fig.add_subplot(121)
    data = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data = pd.DataFrame(data)

    selectdata5 = data.groupby('발생년')
    selectdata6 = selectdata5['발생년'].count()
    x = np.arange(5)
    years = ['2015', '2016', '2017', '2018', '2019']
    values = selectdata6

    plt.bar(x, values)
    plt.xticks(x, years)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response

def chart_hap2(request):
    fig = plt.figure()
    ax = fig.add_subplot(212)  # ax=도화지
    data_df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data_df = pd.DataFrame(data_df)

    df1 = data_df.loc[data_df['발생지시도'] == '충남', ['발생년', '사고유형_대분류']]
    df1_group = df1.groupby("사고유형_대분류")['발생년'].count()
    colors = ['#ffc000', '#8fd9b6', '#d395d0']
    wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}


    ax = df1_group.plot(kind='pie', title='사고유형', figsize=(18, 6), fontsize=17, autopct='%.1f%%', colors=colors,
                        wedgeprops=wedgeprops)

    ax.set_ylabel('', fontsize=5)

    ax = fig.add_subplot(122)  # ax=도화지
    data_df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data_df = pd.DataFrame(data_df)
    df3 = data_df.loc[data_df['발생지시도'] == '충남', ['발생년', '가해자_당사자종별']]
    df3_group = df3.groupby("가해자_당사자종별")['발생년'].count()
    colors1 = ['thistle', 'mistyrose', 'lightpink']

    ax2 = df3_group.plot(kind='pie', title='가해자차종', figsize=(18, 6), fontsize=17, autopct='%.1f%%', colors=colors1)

    ax2.set_ylabel('', fontsize=5)

    ax = fig.add_subplot(121)  # ax=도화지
    data_df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data_df = pd.DataFrame(data_df)
    df5 = data_df.loc[data_df['발생지시도'] == '충남', ['발생년', '피해자_당사자종별']]
    df5_group = df5.groupby("피해자_당사자종별")['발생년'].count()
    df5_group = df5_group.sort_values(ascending=False)
    colors2 = ['darkturquoise', 'cadetblue', 'powderblue', 'lightblue', 'skyblue', 'lightskyblue', 'lightsteelblue',
              'aliceblue', 'linen']

    ax3 = df5_group.plot(kind='pie', title='피해자유형', figsize=(18, 6), fontsize=12, autopct='%.1f%%', colors=colors2)

    ax3.set_ylabel('', fontsize=5)
    ax3.set_ylabel('', fontsize=5)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response

def show_att_vic(request):
    return render(request, 'attacker_victim.html')

def chart_casualtie(request):
    fig = plt.figure()
    ax = fig.add_subplot(121)  # ax=도화지
    data_df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data_df = pd.DataFrame(data_df)
    df4 = data_df.loc[data_df['발생지시도']=='충남',['발생년','발생지시군구']]
    df4_group = df4.groupby("발생지시군구")['발생년'].count()
    df4_group = df4_group.sort_values(ascending=True)
    color = 'rosybrown'

    ax = df4_group.plot(kind='bar', title='시/군별 사고수', figsize=(12, 5), fontsize=13, color=color)
    ax.set_xlabel('', fontsize=12)  # x축 정보 표시

    plt.xticks(rotation=45)  # 가로축 텍스트 회전 (세로로 보이던거 수정)
    ax.set_ylabel('', fontsize=12)  # y축 정보 표시

    ax = fig.add_subplot(122)  # ax=도화지
    data_df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv")

    data_df = pd.DataFrame(data_df)
    df2 = data_df.loc[data_df['발생지시도']=='충남',['발생년','요일']]
    df2_group = df2.groupby("요일")["발생년"].count()
    df2_group = df2_group.sort_values(ascending=False)
    color = 'tan'
    ax5 = df2_group.plot(kind='bar', title='요일별 사고수', figsize=(12, 5), fontsize=18, color=color)
    ax5.set_xlabel('', fontsize=12)  # x축 정보 표시

    plt.xticks(rotation=360)  # 가로축 텍스트 회전 (세로로 보이던거 수정)
    ax5.set_ylabel('', fontsize=12)  # y축 정보 표시

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response

def show_casualties(request):
    return render(request, 'casualties.html')

def open_patients(request):
    return render(request, 'patients.html')

class carouselView(TemplateView):
    template_name = 'carousel.html'
    def get_context_data(self, **kwargs):
        context = super(carouselView, self).get_context_data(**kwargs)
        return context

def law_violations(request):
    fig = plt.figure()
    ax = fig.add_subplot(121)
    df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv", encoding='utf-8')

    data1 = df['가해자법규위반'].value_counts()

    ax = data1.plot(kind='pie', figsize=(15, 10), legend=False, autopct='%1.2f%%', fontsize=12)
    plt.xticks(rotation=0)

    ax = fig.add_subplot(122)

    df = pd.read_csv('C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv', encoding='utf-8')
    data2 = df['가해자법규위반'].value_counts()

    ax1 = data2.plot(kind='bar', figsize=(25, 7), fontsize=9, color='pink')
    ax1.set_xlabel('')
    plt.xticks(rotation=360)  # 가로축 텍스트 회전 (세로로 보이던거 수정)
    ax1.set_ylabel('')

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response

def chart_law(request):
    return render(request, 'law_vioations.html')

def road_shape(request):
    fig = plt.figure()
    ax = fig.add_subplot(121)
    df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv", encoding='utf-8')
    df = pd.DataFrame(df)
    data3=df['도로형태'].value_counts()

    ax = data3.plot(kind='pie', figsize=(15, 10), legend=False, autopct='%1.2f%%', fontsize=15)
    plt.xticks(rotation=0)

    ax = fig.add_subplot(122)
    df = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv", encoding='utf-8')
    df = pd.DataFrame(df)
    data4 = df[df["가해자법규위반"] == "과속"].loc[:, ["가해자법규위반", "도로형태"]].value_counts()

    ax = data4.plot(kind='bar', figsize=(15, 7), legend=False, fontsize=15)
    plt.xticks(rotation=0)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response

def chart_road(request):
    return render(request, 'road_shape.html')

def patients_chart(request):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = pd.read_csv("C:/djangowork1/accidentsite/static/어린이 사망교통사고 정보(2015~2019년).csv", encoding='utf-8')
    df = pd.DataFrame(data)

    chung_df = df.loc[df['발생지시도'] == '충남', ['발생년', '사망자수', '부상자수', '중상자수', '경상자수']]
    chung_group = chung_df.groupby(["발생년"])[["사망자수", "부상자수", "중상자수", "경상자수"]].sum()

    color = "red", "pink", "sandybrown", "peachpuff"
    ax = chung_group.plot(kind='bar', title='환자유형', figsize=(12, 5), legend=True, fontsize=18, color=color)

    ax.set_xlabel('발생년도', fontsize=12)  # x축 정보 표시

    plt.xticks(rotation=45)  # 가로축 텍스트 회전 (세로로 보이던거 수정)
    ax.set_ylabel('사고수', fontsize=12)  # y축 정보 표시
    ax.legend(['사망자수', '부상자수', '경상자수', '중상자수'], fontsize=12)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response










