import pandas as pd
import json

df1 = pd.read_csv('4.csv', encoding='cp949')


def get_df2(gu, dong, job, df):
    if dong == None:
        geo1 = json.load(open(f'{gu}.geojson', encoding='utf-8-sig'))
        df1 = df.copy()
        df1 = df1.drop(['시군구코드', '행정동코드', '행정동명'], axis=1)
        df1 = df1[(df1['서비스업종명'] == job) & (df1['구명'] == gu)]
        data = df1.groupby(['서비스업종명', '코로나구분'], as_index=False).mean()
        covidbefore, covidafter = data[data['코로나구분']
                                       == 0], data[data['코로나구분'] == 1]
        df = pd.read_csv('zzz.csv', encoding='cp949')
        df = df[(df['서비스업종명'] == job) & (df['구명'] == gu)]
        dfani = df
        dfani = dfani.groupby(
            ['서비스업종명', '구명', '행정동', '기준년코드', '기준분기코드'], as_index=False).mean()
        dfani['년도'] = dfani['기준년코드'].map(
            str)+'Y'+' '+dfani['기준분기코드'].map(str)+'Q'
        dfani = dfani.rename(columns={'행정동': 'ADM_DR_NM'})
        sortdf = df.groupby(['서비스업종명', '구명'], as_index=False)['분기당매출액'].sum()
        sortdf = sortdf.sort_values(by=["분기당매출액"], ascending=[False])
        df['년도'] = df['기준년코드'].map(lambda i: str(
            i)[2:])+'년도'+df['기준분기코드'].map(str)+'분기'
        df2 = pd.read_csv('시계열개폐업수.csv', encoding='cp949')
        df2 = df2[(df2['서비스업종명'] == job) & (df2['구명'] == gu)]
        sortdf2 = df2.groupby(['서비스업종명', '구명'], as_index=False)[
            '유사업종점포수'].sum()
        sortdf2 = sortdf2.sort_values(by=["유사업종점포수"], ascending=[False])
        df2['년도'] = df2['기준년코드'].map(lambda i: str(
            i)[2:])+'Y'+' '+df2['기준분기코드'].map(str)+'Q'
        subplotdf = pd.read_csv('1201.csv', encoding='cp949')
        subplotdf = subplotdf[(subplotdf['서비스업종명'] == job)]
        subplotdf = subplotdf[(subplotdf['구명'] == gu)]
        subplotdf = subplotdf.groupby(['년도', '구명'], as_index=False).mean()

        return covidbefore, covidafter, geo1, data, df, df2, dfani, subplotdf

    else:
        df1 = df.copy()
        geo1 = json.load(open(f'{gu}.geojson', encoding='utf-8-sig'))
        df1 = df1[df1['행정동명'] == dong]
        df1 = df1.drop(['시군구코드', '행정동코드'], axis=1)
        df1 = df1.groupby(['서비스업종명', '행정동명', '코로나구분'], as_index=False).mean()
        data = df1[(df1['서비스업종명'] == job)]
        data = data.rename(columns={'행정동명': 'ADM_DR_NM'})
        covidbefore = data[data['코로나구분'] == 0]
        covidafter = data[data['코로나구분'] == 1]
        df = pd.read_csv('zzz.csv', encoding='cp949')
        df = df[(df['서비스업종명'] == job) & (df['구명'] == gu)]
        dfani = df
        dfani = dfani.groupby(
            ['서비스업종명', '구명', '행정동', '기준년코드', '기준분기코드'], as_index=False).mean()
        dfani['년도'] = dfani['기준년코드'].map(lambda i: str(
            i)[2:])+'Y'+' '+dfani['기준분기코드'].map(str)+'Q'
        dfani = dfani.rename(columns={'행정동': 'ADM_DR_NM'})

        sortdf = df.groupby(['서비스업종명', '구명', '행정동'], as_index=False)[
            '분기당매출액'].sum()
        sortdf = sortdf.sort_values(by=["분기당매출액"], ascending=[False])
        legend = (sortdf['행정동'][:5].values).tolist()
        df['년도'] = df['기준년코드'].map(lambda i: str(
            i)[2:])+'Y'+' '+df['기준분기코드'].map(str)+'Q'
        df = df.query('''행정동 == @legend''')
        df2 = pd.read_csv('시계열개폐업수.csv', encoding='cp949')
        df2 = df2[(df2['서비스업종명'] == job) & (df2['구명'] == gu)]
        sortdf2 = df2.groupby(['서비스업종명', '구명', '행정동'], as_index=False)[
            '유사업종점포수'].sum()
        sortdf2 = sortdf2.sort_values(by=["유사업종점포수"], ascending=[False])
        legend2 = (sortdf2['행정동'][:5].values).tolist()
        df2['년도'] = df2['기준년코드'].map(lambda i: str(
            i)[2:])+'Y'+' '+df2['기준분기코드'].map(str)+'Q'
        df2 = df2.query('''행정동 == @legend2''')
        subplotdf = pd.read_csv('1201.csv', encoding='cp949')
        subplotdf = subplotdf[(subplotdf['서비스업종명'] == job)]
        subplotdf = subplotdf[(subplotdf['구명'] == gu) &
                              (subplotdf['행정동명'] == dong)]

        return covidbefore, covidafter, geo1, data, df, df2, dfani, subplotdf


def get_df1(job, df):
    dftotal = df.copy()
    geototal = json.load(open('seoulGu.geojson', encoding='utf-8-sig'))
    dftotal = dftotal.drop(['시군구코드', '행정동코드'], axis=1)
    dftotal = dftotal[(dftotal['서비스업종명'] == job)]
    dftotal = dftotal.groupby(
        ['서비스업종명', '구명', '코로나구분'], as_index=False).mean()
    covidbefore_total = dftotal[dftotal['코로나구분'] == 0]
    covidafter_total = dftotal[dftotal['코로나구분'] == 1]
    dftotal2 = pd.read_csv('zzz.csv', encoding='cp949')
    dftotal2 = dftotal2[(dftotal2['서비스업종명'] == job)]
    sortdf_total = dftotal2.groupby(['서비스업종명', '구명'], as_index=False)[
        '분기당매출액'].sum()
    sortdf_total = sortdf_total.sort_values(by=["분기당매출액"], ascending=[False])
    df7 = pd.read_csv('zzz.csv', encoding='cp949')
    df7 = df7[(df7['서비스업종명'] == job)]
    df7 = df7.groupby(['구명', '기준년코드', '기준분기코드'], as_index=False)[
        '분기당매출액'].mean()
    df7['년도'] = df7['기준년코드'].map(lambda i: str(
        i)[2:])+'Y'+' '+df7['기준분기코드'].map(str)+'Q'
    df7 = df7.rename(columns={'구명': 'SIG_KOR_NM'})
    dftotal2 = dftotal2.groupby(
        ['서비스업종명', '구명', '기준년코드', '기준분기코드'], as_index=False)['분기당매출액'].sum()
    legend_total = (sortdf_total['구명'][:5].values).tolist()
    dftotal2['년도'] = dftotal2['기준년코드'].map(lambda i: str(
        i)[2:])+'Y'+' '+dftotal2['기준분기코드'].map(str)+'Q'
    yeardf_total = dftotal2.query('''구명 == @legend_total''')
    dfshop_total = pd.read_csv('시계열개폐업수.csv', encoding='cp949')
    dfshop_total = dfshop_total[(dfshop_total['서비스업종명'] == job)]
    dfshop_total['년도'] = dfshop_total['기준년코드'].map(
        lambda i: str(i)[2:])+'Y'+' '+dfshop_total['기준분기코드'].map(str)+'Q'
    sortdf_total2 = dfshop_total.groupby(
        ['서비스업종명', '구명'], as_index=False)['유사업종점포수'].sum()
    sortdf_total2 = sortdf_total2.sort_values(
        by=["유사업종점포수"], ascending=[False])
    legend_total2 = (sortdf_total2['구명'][:5].values).tolist()
    dfshop_total = dfshop_total.groupby(
        ['서비스업종명', '년도', '구명'], as_index=False)['유사업종점포수'].sum()
    dfshop_total = dfshop_total.query('''구명 == @legend_total2''')
    total_subplotdf = pd.read_csv('1201.csv', encoding='cp949')
    total_subplotdf = total_subplotdf[(total_subplotdf['서비스업종명'] == job)]
    total_subplotdf = total_subplotdf.groupby(['년도'], as_index=False).mean()

    return covidbefore_total, covidafter_total, geototal, yeardf_total, dfshop_total, df7, dftotal, total_subplotdf


def total_dong_sort():
    total_dong = pd.read_csv('행정동순위.csv', encoding='utf-8')
    sorted_dong_df = total_dong.drop(['점포당평균매출액', '이전점포당평균매출액'], axis=1)
    sorted_dong_df['변동률(%)'] = sorted_dong_df['변동률'].map(str)+'%'
    sorted_dong_df_up = sorted_dong_df.sort_values(
        by=['변동률'], ascending=True).head(5)
    sorted_dong_df_up = sorted_dong_df_up.drop(['변동률'], axis=1)
    sorted_dong_df_down = sorted_dong_df.sort_values(
        by=['변동률'], ascending=False).head(5)
    sorted_dong_df_down = sorted_dong_df_down.drop(['변동률'], axis=1)

    return sorted_dong_df_up, sorted_dong_df_down


def total_job_sort():
    total_job = pd.read_csv('서비스업종순위.csv', encoding='utf-8')
    sorted_job_df = total_job.drop(['점포당평균매출액', '이전점포당평균매출액'], axis=1)
    sorted_job_df['변동률(%)'] = sorted_job_df['변동률'].map(str)+'%'
    sorted_job_df_up = sorted_job_df.sort_values(
        by=['변동률'], ascending=True).head(5)
    sorted_job_df_up = sorted_job_df_up.drop(['변동률'], axis=1)
    sorted_job_df_down = sorted_job_df.sort_values(
        by=['변동률'], ascending=False).head(5)
    sorted_job_df_down = sorted_job_df_down.drop(['변동률'], axis=1)

    return sorted_job_df_up, sorted_job_df_down
