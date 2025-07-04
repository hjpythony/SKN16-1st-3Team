
def show_page_4():

  import streamlit as st
  import plotly.express as px
  import pandas as pd
  import sqlite3
  import matplotlib.pyplot as plt
  import plotly.express as px
  import seaborn as sns
  import numpy as np
  import matplotlib.font_manager as fm


  #폰트 설정
  font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
  fontprop = fm.FontProperties(fname=font_path, size=10)
  plt.rcParams['font.family'] = 'NanumGothic'
  plt.rcParams['axes.unicode_minus'] = False


  #sqlite 메모리 DB 생성
  conn = sqlite3.connect(':memory:')

  #sql 파일 읽기
  with open('/content/SQL/ev.sql', 'r', encoding='utf-8') as f:
      sql_script = f.read()

  #sql 스크립트 실행 (테이블 생성 + 데이터 삽입)
  conn.executescript(sql_script)

  # 쿼리 실행 후 데이터프레임으로 변환
  df_charger = pd.read_sql_query('SELECT * FROM charger where year=2024 and month =12', conn)
  df_ev = pd.read_sql_query('SELECT * FROM ev where year=2024 and month =12', conn)

  print(df_charger.head())

  print(df_ev.head())


  # 날짜 컬럼 생성
  df_charger['날짜'] = pd.to_datetime(df_charger[['year', 'month']].assign(day=1))
  df_ev['날짜'] = pd.to_datetime(df_ev[['year', 'month']].assign(day=1))

  print(df_charger['날짜'])
  print(df_ev['날짜'])

  # 📊 전체 기간 누적된 충전기 수 / 차량 수 비율 시각화

  # 누적 집계
  charger_summary = df_charger.groupby('region', as_index=False)['charger_count'].sum()
  ev_summary = df_ev.groupby('region', as_index=False)['ev_count'].sum()

  # 병합 및 차량당 충전기 수 계산
  merged_df = pd.merge(ev_summary, charger_summary, on='region')
  merged_df['차량당_충전기_수'] = merged_df['charger_count'] / merged_df['ev_count']

  #merged_df_sorted = merged_df.sort_values('차량당_충전소_수', ascending=True)


  # 막대그래프 (Plotly)
  fig = px.bar(
      merged_df.sort_values('차량당_충전기_수', ascending=False),
      x='차량당_충전기_수',
      y='region',
      orientation='h',
      text='차량당_충전기_수',
      hover_data={
          'region': True,
          'ev_count': True,
          'charger_count': True,
          '차량당_충전기_수': ':.4f'
      },
      color='차량당_충전기_수',
      color_continuous_scale='Greens'
  )

  fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
  fig.update_layout(
      title={
          'text': '2024년 12월기준 - 지역별 차량당 충전기 수',
          'x': 0.5,
          'xanchor': 'left',
          'font': dict(
              size=18,
              family='NanumGothic',
              color='black'
          )
      },
      xaxis_title='차량당 충전기 수',
      yaxis_title='지역',
      coloraxis_showscale=False,
      height=600
  )

  st.plotly_chart(fig, use_container_width=True)




  # st.subheader("전체 기간 누적된 충전기 수 / 차량 수 비율")
  # fig1, ax1 = plt.subplots(figsize=(10, 8))
  # ax1.barh(merged_df_sorted['region'], merged_df_sorted['차량당_충전소_수'], color='mediumseagreen')
  # ax1.set_xlabel('차량당 충전기 수')
  # ax1.set_title('지역별 차량당 충전기 수')
  # st.pyplot(fig1)




  # 📈 시기별 변화 분석
  # 지역 + 날짜별로 집계
  charger_by_time = df_charger.groupby(['region', '날짜'])['charger_count'].sum().reset_index()
  ev_by_time = df_ev.groupby(['region', '날짜'])['ev_count'].sum().reset_index()

  # 병합
  merged_time = pd.merge(ev_by_time, charger_by_time, on=['region', '날짜'])
  merged_time['차량당_충전기_수'] = merged_time['charger_count'] / merged_time['ev_count']

  # ✅ Streamlit: 사용자 지역 선택
  region_list = merged_time['region'].unique().tolist()
  selected_region = st.selectbox("지역 선택 (시계열 보기)", region_list)

  # 해당 지역 시계열 그래프
  df_selected = merged_time[merged_time['region'] == selected_region]

  st.subheader(f"{selected_region} - 시기별 차량당 충전기 수 변화")
  fig2, ax2 = plt.subplots(figsize=(10, 5))
  ax2.plot(df_selected['날짜'], df_selected['차량당_충전기_수'], marker='o', color='orange')
  ax2.set_ylabel("차량당 충전기 수")
  ax2.set_xlabel("날짜")
  ax2.set_title(f"{selected_region}의 시기별 차량당 충전기 수 추이")
  ax2.grid(True)
  st.pyplot(fig2)
