import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
from io import BytesIO
import os
import base64
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('font', family='Malgun Gothic')

data_path = 'C:/Users/82104/Desktop/상권예측/gu'

os.chdir(data_path)


def log_graph(df):
    img = BytesIO()
    fig = plt.figure(figsize=(10, 10))
    plt.subplot(311)
    sns.countplot(x='업종', data=(df[df['업종'] != 'False']),
                  order=df['업종'].value_counts().index[1:6], palette="Set2")
    plt.title('업종 검색횟수', fontsize=18)
    plt.xlabel('업종', fontsize=15)
    plt.ylabel('검색횟수', fontsize=15)
    plt.subplot(312)
    sns.countplot(x='구', data=(df[df['구'] != 'False']),
                  order=df['구'].value_counts().index[1:6], palette="Set2")
    plt.title('구 검색횟수', fontsize=18)
    plt.xlabel('구', fontsize=15)
    plt.ylabel('검색횟수', fontsize=15)
    plt.subplot(313)
    sns.countplot(x='동', data=(df[df['동'] != 'False']),
                  order=df['동'].value_counts().index[1:6], palette="Set2")
    plt.title('동 검색횟수', fontsize=18)
    plt.xlabel('동', fontsize=15)
    plt.ylabel('검색횟수', fontsize=15)

    plt.tight_layout()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url


def get_graph1(df, xlabel, ylabel, legend):
    # colors = ['#03588C'] * len(df.index)
    # colors[2] = '#F24472'

    # low = df.values * 0.8
    colors = '#91C6E6'
    colors2 = '#BEE3E4'

    fig = px.bar(df, x=xlabel, y=ylabel, color=legend,
                 barmode='stack', height=350, width=350)
    # 그룹화 시킨 graph

    fig.update_layout({
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': '#FFFFFF',
    }, font_size=15, font_color='#60606E', font_family='Franklin Gothic', showlegend=False)
    fig.update_traces(marker={"color": colors},
                      selector={'name': '이전'}, width=0.5)
    fig.update_traces(marker={"color": colors2},
                      selector={'name': '이후'}, width=0.5)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        title='시간대별 매출액',
        title_font_size=23,
        title_yanchor='top'
    )

    fig.update_xaxes(title=None, visible=True, showticklabels=True)
    fig.update_yaxes(title=None, visible=True, showticklabels=True)
    return fig


def get_graph3(df, xlabel, ylabel, legend):

    colors = '#91C6E6'
    colors2 = '#BEE3E4'

    fig = px.bar(df, y=xlabel, x=ylabel, color=legend, barmode='group')
    # 그룹화 시킨 graph
    # replaces default labels by column name

    fig.update_layout({
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': '#FFFFFF',
    }, font_size=15, font_color='#60606E', font_family='Franklin Gothic')
    fig.update_traces(marker={"color": colors},
                      selector={'name': '이전'}, width=0.5)
    fig.update_traces(marker={"color": colors2},
                      selector={'name': '이후'}, width=0.5)
    fig.update_layout({
        'title': '연령대별 매출액',
        'title_font_size': 34,
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': '#FFFFFF',
    }, title_y=0.93)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    #fig.update_xaxes(title='', visible=True,showticklabels=True)
    #fig.update_yaxes(title='', visible=True,showticklabels=True)
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    return fig


def get_graph2(df, xlabel, ylabel, legend):
    colors = ['#91C6E6']
    colors2 = ['#BEE3E4']

    fig = px.bar_polar(df, r=ylabel, theta=xlabel, color=legend,
                       color_discrete_sequence=['#91C6E6', '#BEE3E4'],
                       height=350, width=350
                       )
    fig.update_layout(
        title='요일별 매출액',
        title_font_size=23,
        title_yanchor='top'
    )

    fig.update_layout(polar=dict(radialaxis=dict(
        showticklabels=False, ticks='', linewidth=0)))
    fig.update_layout(showlegend=False, font_size=17,
                      font_color='#60606E', font_family='Franklin Gothic')

    # fig = fig.update_axes(showticklabels=False)
    return fig


def graph_set1(dfani, gu):

    geo1 = json.load(open(f'{gu}.geojson', encoding='utf-8-sig'))
    mapbox = px.choropleth(dfani, geojson=geo1, locations='ADM_DR_NM', color='분기당매출액', color_continuous_scale='Blues',
                           featureidkey='properties.ADM_DR_NM', animation_frame='년도')
    mapbox = mapbox.update_geos(fitbounds='locations', visible=False)
    mapbox.add_scattergeo(
        geojson=geo1,
        locations=list(dfani.ADM_DR_NM),
        text=list(dfani.ADM_DR_NM),
        featureidkey="properties.ADM_DR_NM",
        mode='text')
    mapbox.update_layout(font_size=15, font_color='#60606E',
                         font_family='Franklin Gothic')
    return mapbox


def graph_set2(covidbefore, covidafter, geo1, data):
    times = [time for time in data.loc[:,
                                       '시간대00~06평균매출액':'시간대21~24평균매출액'].columns]
    df_times = pd.DataFrame({
        '시간대': [time[3:8] for time in times] * 2,
        '매출액': [covidbefore[time].sum() for time in times] + [covidafter[time].sum() for time in times],
        '코로나': ['이전' for _ in range(6)] + ['이후' for _ in range(6)]})
    graph_times = get_graph1(df_times, '시간대', '매출액', '코로나')

    return graph_times


def graph_set3(df):
    graph_byyear = px.line(df, x='년도', y="분기당매출액",
                           color='행정동', title="재미있는 코딩")
    return graph_byyear


def graph_set4(df2):
    graph_shop = px.line(df2, x='년도', y='유사업종점포수', color='행정동')
    return graph_shop


def graph_set6(covidbefore, covidafter, geo1, data):
    days = [week for week in data.loc[:, '월요일평균매출액':'일요일평균매출액'].columns]
    df_days = pd.DataFrame({
        '요일별': [day[:3] for day in days] * 2,
        '매출액': [covidbefore[day].sum() for day in days] + [covidafter[day].sum() for day in days],
        '코로나': ['이전' for _ in range(7)] + ['이후' for _ in range(7)]})
    graph_days = get_graph2(df_days, '요일별', '매출액', '코로나')

    return graph_days


def graph_set7(covidbefore, covidafter, geo1, data):
    ages = [age for age in data.loc[:, '10대평균매출액':'60대이상평균매출액'].columns]
    df_ages = pd.DataFrame({
        '연령별': [age[:3] for age in ages] * 2,
        '매출액': [covidbefore[age].sum() for age in ages] + [covidafter[age].sum() for age in ages],
        '코로나': ['이전' for _ in range(6)] + ['이후' for _ in range(6)]})
    graph_ages = get_graph3(df_ages, '연령별', '매출액', '코로나')

    return graph_ages


def total_get_graph(df, xlabel, ylabel, legend):

    # low = df.values * 0.8
    high = df['매출액'].idxmax()
    colors = ['#F24472' if i == high else '#03588C' for i in df.index]

    fig = px.bar(df, x=xlabel, y=ylabel, color=legend, barmode='group')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })

    fig.update_traces(marker={"color": colors},
                      selector={'name': '이전'}, width=0.5)
    fig.update_traces(marker={"color": colors},
                      selector={'name': '이후'}, width=0.5)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig


def total_graph_set1(df7):
    geototal = json.load(open('seoulGu.geojson', encoding='utf-8-sig'))
    for i in range(len(geototal['features'])):
        if geototal['features'][i]['properties']['SIG_KOR_NM'] not in list(df7.SIG_KOR_NM):
            df7 = df7.append(
                {'SIG_KOR_NM': geototal['features'][i]['properties']['SIG_KOR_NM']}, ignore_index=True)
            df7 = df7.fillna(0)
    mapbox_total = px.choropleth(df7, geojson=geototal, locations='SIG_KOR_NM', color='분기당매출액', color_continuous_scale='Blues',
                                 featureidkey='properties.SIG_KOR_NM', animation_frame='년도')
    mapbox_total = mapbox_total.update_geos(
        fitbounds='locations', visible=False)
    mapbox_total.add_scattergeo(
        geojson=geototal,
        locations=list(df7.SIG_KOR_NM),
        text=list(df7.SIG_KOR_NM),
        featureidkey="properties.SIG_KOR_NM",
        mode='text')
    return mapbox_total


def total_graph_set2(covidbefore_total, covidafter_total,  dftotal):
    times = [time for time in dftotal.iloc[:, 5:10].columns]
    df_times = pd.DataFrame({
        '시간대': [time[3:8] for time in times] * 2,
        '매출액': [covidbefore_total[time].sum() for time in times] + [covidafter_total[time].sum() for time in times],
        '코로나': ['이전' for _ in range(5)] + ['이후' for _ in range(5)]})
    total_graph_times = get_graph1(df_times, '시간대', '매출액', '코로나')

    return total_graph_times


def total_graph_set3(yeardf_total):

    total_graph_byyear = px.line(yeardf_total, x='년도', y="분기당매출액", color='구명')

    return total_graph_byyear


def total_graph_set4(dfshop_total):

    total_graph_shop = px.line(dfshop_total, x='년도', y='유사업종점포수', color='구명')

    return total_graph_shop


def total_graph_set6(covidbefore_total, covidafter_total, dftotal):
    days = [week for week in dftotal.iloc[:, -7:].columns]
    df_days = pd.DataFrame({
        '요일별': [day[:3] for day in days] * 2,
        '매출액': [covidbefore_total[day].sum() for day in days] + [covidafter_total[day].sum() for day in days],
        '코로나': ['이전' for _ in range(7)] + ['이후' for _ in range(7)]})
    total_graph_days = get_graph2(df_days, '요일별', '매출액', '코로나')

    return total_graph_days


def total_graph_set7(covidbefore_total, covidafter_total,  dftotal):
    ages = [age for age in dftotal.iloc[:, 10:-9].columns]
    df_ages = pd.DataFrame({
        '연령별': [age[:3] for age in ages] * 2,
        '매출액': [covidbefore_total[age].sum() for age in ages] + [covidafter_total[age].sum() for age in ages],
        '코로나': ['이전' for _ in range(6)] + ['이후' for _ in range(6)]})
    total_graph_ages = get_graph3(df_ages, '연령별', '매출액', '코로나')

    return total_graph_ages


# 갑영누나 파일 추가


def graph_set5(subplotdf):
    colors = '#91C6E6'
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    subfig = subfig.add_trace(
        go.Bar(x=subplotdf['년도'], y=subplotdf['점포수'], name='점포수'), secondary_y=False)
    subfig = subfig.add_trace(go.Scatter(
        x=subplotdf['년도'], y=subplotdf['점포당평균매출액'], name='매출액', line=dict(color='#000080', width=4), mode='lines'), secondary_y=True,)
    subfig.update_layout({
        'title': '점포수-매출액',
        'title_font_size': 34,
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': '#FFFFFF',
    }, font_size=15, font_color='#60606E', font_family='Franklin Gothic')
    subfig.update_traces(marker={"color": colors}, selector={'name': '점포수'})

    # total_subfig.update_traces(marker={"color": colors}, selector={'name': '이전'})
    # fig.update_traces(marker={"color": colors2}, selector={'name': '이후'})

    subfig.update_xaxes(showgrid=False)
    subfig.update_yaxes(showgrid=False)
    return subfig


# 갑영누나 파일 추가
def total_graph_set5(total_subplotdf):
    colors = '#91C6E6'
    total_subfig = make_subplots(specs=[[{"secondary_y": True}]])
    total_subfig = total_subfig.add_trace(go.Bar(
        x=total_subplotdf['년도'], y=total_subplotdf['점포수'], name='점포수'), secondary_y=False)
    total_subfig = total_subfig.add_trace(go.Scatter(
        x=total_subplotdf['년도'], y=total_subplotdf['점포당평균매출액'], name='매출액', line=dict(color='#000080', width=4), mode='lines'), secondary_y=True,)
    total_subfig.update_layout({
        'title': '점포수-매출액',
        'title_font_size': 34,
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': '#FFFFFF',
    }, font_size=15, font_color='#60606E', font_family='Franklin Gothic')
    total_subfig.update_traces(
        marker={"color": colors}, selector={'name': '점포수'})

    return total_subfig
