from graph import *
from df import *
from dash import Dash
from dash import dcc
from dash import html
import sqlite3
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from dash import dash_table

app = Flask(__name__)
# app.config["SECRET_KEY"] = "ABCD"
dash_app = Dash(server=app, url_base_pathname='/dash/')
gu, dong, job = '강남구', '신사동', '중식음식점'


def layout(gu, dong, job, graph_days, graph_times, graph_ages, mapbox, graph_byyear, graph_shop):
    # 갑영누나가 준 파일
    sorted_dong_df_up, sorted_dong_df_down = total_dong_sort()
    sorted_job_df_up, sorted_job_df_down = total_job_sort()
    auto_text_list = []
    auto_text_list.append([gu, dong, job])

    if gu == None:
        auto_text_list[0][0] = ''
        auto_text_list[0][1] = ''

    con = sqlite3.connect('./log.db')
    cur = con.cursor()
    cur.execute(
        "SELECT 업종, count(업종) FROM log GROUP BY 업종 ORDER BY count(업종) DESC;")
    datas_job = cur.fetchall()
    cur.execute(
        "SELECT 구, count(구) FROM log GROUP BY 구 ORDER BY count(구) DESC;")
    datas_gu = cur.fetchall()
    cur.execute(
        "SELECT 동, count(동) FROM log GROUP BY 동 ORDER BY count(동) DESC;")
    datas_dong = cur.fetchall()

    con.commit()
    con.close()

    # 추가
    res = []
    for i in range(3):
        res.append([datas_dong[i][0], datas_dong[i][1]])
        res.append([datas_gu[i][0], datas_gu[i][1]])
        res.append([datas_job[i][0], datas_job[i][1]])

    dash_app.layout = html.Meta(
        content="width=device-width, initial-scale=1.0")

    dash_app.layout = html.Div(
        id="super-sheet",
        children=[
            html.Div(  # main-tilte
                "서울특별시 " + auto_text_list[0][0] + " " + auto_text_list[0][1] + " " + auto_text_list[0][2] + " 분류별 추이", className="main-title", id="main-title",
            ),
            html.Div(  # contents-arear
                id="contents-area",
                children=[
                    html.Div(
                        id="upper-contents",
                        children=[html.Div([
                            dcc.Graph(id='fuck',
                                  figure=graph_ages, style={
                                      'height': '43.6%', 'bottom': '100px'}
                                      ),
                            # html.Div('graph 2', className="upper-left-second-Graph")
                            dcc.Graph(
                                id='ssibal',
                                figure=graph_days,
                            ),
                        ]),
                            html.Div(
                            id="upper-contents-mid",
                            # html.Div("2", className="upper-mid-map")
                            children=[
                                html.Div(
                                    dcc.Graph(
                                        id='example-graph4',
                                        className="upper-mid-map",
                                        figure=mapbox,
                                        style={'height': "100%"}
                                    ), style={'height': "100%"}
                                )
                            ]),

                            html.Div(
                            id="upper-contents-right",
                            children=[
                                html.Div("자치구 상·하위 변동률",
                                         className="upper-right-sub-title"),
                                html.Div(
                                    className="upper-right-flex",
                                    children=[
                                        html.Div(
                                            className="upper-right-table",
                                            children=[
                                                dash_table.DataTable(
                                                    id='table',
                                                    columns=[{"name": i, "id": i}
                                                             for i in sorted_dong_df_down.columns],
                                                    data=sorted_dong_df_down.to_dict(
                                                        'records'),
                                                    editable=True,
                                                    style_data={
                                                        'color': 'black',
                                                        'backgroundColor': 'white'
                                                    },
                                                    style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'odd'},
                                                            'backgroundColor': 'rgb(220, 220, 220)',
                                                        }
                                                    ],
                                                    style_header={
                                                        'backgroundColor': 'rgb(210, 210, 210)',
                                                        'color': 'black',
                                                                 'fontWeight': 'bold'
                                                    },
                                                    style_cell={
                                                        'textAlign': 'center'}
                                                )
                                            ]),
                                        html.Div(
                                            className="upper-right-table",
                                            children=[
                                                dash_table.DataTable(
                                                    id='table',
                                                    columns=[{"name": i, "id": i}
                                                             for i in sorted_dong_df_up.columns],
                                                    data=sorted_dong_df_up.to_dict(
                                                        'records'),
                                                    editable=True,
                                                    style_data={
                                                        'color': 'black',
                                                        'backgroundColor': 'white'
                                                    },
                                                    style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'odd'},
                                                            'backgroundColor': 'rgb(220, 220, 220)',
                                                        }
                                                    ],
                                                    style_header={
                                                        'backgroundColor': 'rgb(210, 210, 210)',
                                                        'color': 'black',
                                                        'fontWeight': 'bold'
                                                    },
                                                    style_cell={
                                                        'textAlign': 'center'}
                                                )
                                            ])
                                    ]),
                                html.Div("선택 업종 상·하위 변동률",
                                         className="upper-right-sub-title"),
                                html.Div(
                                    className="upper-right-flex",
                                    children=[
                                        html.Div(
                                            className="upper-right-table",
                                            children=[
                                                dash_table.DataTable(
                                                    id='table',
                                                    columns=[{"name": i, "id": i}
                                                             for i in sorted_job_df_down.columns],
                                                    data=sorted_job_df_down.to_dict(
                                                        'records'),
                                                    editable=True,
                                                    style_data={
                                                        'color': 'black',
                                                        'backgroundColor': 'white'
                                                    },
                                                    style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'odd'},
                                                            'backgroundColor': 'rgb(220, 220, 220)',
                                                        }
                                                    ],
                                                    style_header={
                                                        'backgroundColor': 'rgb(210, 210, 210)',
                                                        'color': 'black',
                                                                 'fontWeight': 'bold'
                                                    },
                                                    style_cell={
                                                        'textAlign': 'center'}
                                                )
                                            ]),
                                        html.Div(
                                            className="upper-right-table",
                                            children=[
                                                dash_table.DataTable(
                                                    id='table',
                                                    columns=[{"name": i, "id": i}
                                                             for i in sorted_job_df_up.columns],
                                                    data=sorted_job_df_up.to_dict(
                                                        'records'),
                                                    editable=True,
                                                    style_data={
                                                        'color': 'black',
                                                        'backgroundColor': 'white'
                                                    },
                                                    style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'odd'},
                                                            'backgroundColor': 'rgb(220, 220, 220)',
                                                        }
                                                    ],
                                                    style_header={
                                                        'backgroundColor': 'rgb(210, 210, 210)',
                                                        'color': 'black',
                                                                 'fontWeight': 'bold'
                                                    },
                                                    style_cell={
                                                        'textAlign': 'center'}
                                                )
                                            ])
                                    ]),
                            ]),
                        ]),
                ]),
            html.Div(
                id="lower-contents",
                children=[
                    # html.Div("con1", className="lower-contents-left"),
                    html.Div(
                        dcc.Graph(
                            id='example-graph99',
                            # className="lower-contents-left",
                            figure=graph_times,
                            style={'height': "100%"},
                        ), style={'height': "100%", 'width': "50%", "padding": "10px 10px 10px 10px"}
                    ),

                    # html.Div("con2", className="lower-contents-right")
                    html.Div(
                        dcc.Graph(
                            id='example-graph99',
                            # className="lower-contents-right",
                            figure=graph_shop,
                            style={'height': "100%"},
                        ), style={'height': "100%", 'width': "50%", "padding": "10px 10px 10px 10px"}
                    )
                ])
        ])


dash_app.layout = html.Div([
    dcc.Upload(
        id='datatable-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        },
    ),
    dash_table.DataTable(id='datatable-upload-container'),
    html.Div(dcc.Graph(id="my-graph"))
])


@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == "GET":
        return render_template('home.html')
    else:
        # 리퀘스트를 받아옵니다.
        tabs = request.form.get('tabs', False)  # 서울시 전체보기 / 지역별 비교
        gu = request.form.get('location', False)  # 지역구 선택
        dong = request.form.get('dong', False)  # 동 선택 (전체 / 동선택)
        job = request.form.get('service', False)  # 서비스 선택

        # 리퀘스트값을 데이터베이스에 저장합니다.
        con = sqlite3.connect('./log.db')
        cur = con.cursor()
        con.execute(
            "CREATE TABLE IF NOT EXISTS log (탭 TEXT, 업종 TEXT, 구 TEXT, 동 TEXT)")
        cur.execute(
            f"INSERT INTO log (업종,구,동) VALUES('{job}','{gu}','{dong}')")
        con.commit()
        con.close()

        # 지역별 비교
        if tabs == '지역구 매출액 비교':
            # 지역구별 매출비교 탭에서 인풋이 누락되면 에러메시지를 띄웁니다.
            if (gu == False) or (dong == False) or (job == False):
                flash("Please select!")
                return render_template('home.html')
            else:
                # 데이터를 호출하고 대쉬레이어 함수에 파라미터로 넣습니다.
                # 사용자가 구 전체의 데이터를 비교합니다.
                if dong == '전체':
                    covidbefore2, covidafter2, geo1_2, data_2, df, df2, dfani, subplotdf = get_df2(
                        gu, None, job, df1)
                    graph1 = graph_set2(
                        covidbefore2, covidafter2, geo1_2, data_2)
                    graph2 = graph_set7(
                        covidbefore2, covidafter2, geo1_2, data_2)
                    graph3 = graph_set6(
                        covidbefore2, covidafter2, geo1_2, data_2)
                    graph4 = graph_set1(dfani, gu)
                    graph5 = graph_set3(df)
                    graph6 = graph_set5(subplotdf)
                    layout(gu, dong, job, graph1, graph2,
                           graph3, graph4, graph5, graph6)
                    return redirect(url_for('/dash/'))

                # 사용자가 구 내의 동 전체의 데이터를 비교합니다.
                else:
                    covidbefore, covidafter, geo1, data, df, df2, dfani, subplotdf = get_df2(
                        gu, dong, job, df1)
                    graph1 = graph_set2(
                        covidbefore, covidafter, geo1, data)
                    graph2 = graph_set7(covidbefore, covidafter, geo1, data)
                    graph3 = graph_set6(covidbefore, covidafter, geo1, data)
                    graph4 = graph_set1(dfani, gu)
                    graph5 = graph_set3(df)
                    graph6 = graph_set5(subplotdf)
                    layout(gu, dong, job, graph1, graph2,
                           graph3, graph4, graph5, graph6)
                    return redirect(url_for('/dash/'))
        # 서울시 전체 데이터 보기
        elif tabs == '서울시 전체':
            # 업종 누락시 에러메시지를 띄웁니다.
            if job == False:
                flash("Please select!")
                return render_template('home.html')
            else:
                covidbefore_total, covidafter_total, geototal, yeardf_total, dfshop_total, df7, dftotal, total_subplotdf = get_df1(
                    job, df1)
                total_graph1 = total_graph_set2(
                    covidbefore_total, covidafter_total, dftotal)
                total_graph2 = total_graph_set7(
                    covidbefore_total, covidafter_total, dftotal)
                total_graph3 = total_graph_set6(
                    covidbefore_total, covidafter_total, dftotal)
                total_graph4 = total_graph_set1(df7)
                total_graph5 = total_graph_set3(yeardf_total)
                total_graph6 = total_graph_set5(total_subplotdf)
                layout(None, None, job, total_graph1, total_graph2,
                       total_graph3, total_graph4, total_graph5, total_graph6)

                return redirect(url_for('/dash/'))
       # 로그기록을 확인합니다.(인기 검색 순위)
        else:
            return redirect(url_for('list'))


@app.route('/list')
def list():
    con = sqlite3.connect('log.db')
    cur = con.cursor()
    df = pd.read_sql_query("SELECT * FROM log", con)
    cur.execute("SELECT * FROM log")
    # 로그초기화
    # cur.execute("DELETE FROM log;")
    datas = cur.fetchall()
    con.commit()
    con.close()

    res = []
    for data in datas:
        new_dict = {
            "업종": data[0],
            "구": data[1],
            "동": data[2],
        }
        res.append(new_dict)

    job = df[df['업종'] != 'False']['업종'].value_counts().sort_values(ascending=False)[
        :5]
    gu = df[df['구'] != 'False']['구'].value_counts().sort_values(ascending=False)[
        :5]
    # .value_counts().rename_axis('unique_values').reset_index(name='counts')
    dong = df[df['동'] != 'False']['동'].value_counts().sort_values(ascending=False)[
        :5]

    plot_url = log_graph(df)
    return render_template('log.html', plot_url=plot_url, job=job, gu=gu, dong=dong)


@app.route('/dash/')
def dash1():
    return dash_app


if __name__ == '__main__':
    app.run(debug=True)
