import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import sqlite3
import pandas as pd

font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path, size=10)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False


def show_page_2():
    
  st.set_page_config(page_title="전기차/충전기 시각화", layout="centered")
  st.title("📊 지역별 전기차 등록 대수 및 충전기 개수 비교")

  #sqlite 메모리 DB 생성
  conn = sqlite3.connect(':memory:')

  #sql 파일 읽기
  with open('/content/SQL/ev.sql', 'r', encoding='utf-8') as f:
      sql_script = f.read()

  #sql 스크립트 실행 (테이블 생성 + 데이터 삽입)
  conn.executescript(sql_script)

  #쿼리 실행 후 데이터프레임으로 변환
  df_charger = pd.read_sql_query('SELECT region, SUM(charger_count) AS charger_count FROM charger WHERE YEAR = 2024 AND MONTH =12 GROUP BY region', conn)
  df_ev = pd.read_sql_query('SELECT region, ev_count FROM ev WHERE YEAR = 2024 AND MONTH=12', conn)

  print(df_charger)

  print(df_ev.head)


  # 📌 데이터 병합
  df_merged = pd.merge(df_ev, df_charger, on='region')

  # 📌 정렬 (옵션)
  region_order = ['서울', '경기', '인천', '경상', '전라', '충청', '강원', '제주']
  df_merged['region'] = pd.Categorical(df_merged['region'], categories=region_order, ordered=True)
  df_merged = df_merged.sort_values('region')

  # 📌 시각화용 데이터 추출
  regions = df_merged['region'].tolist()
  ev_counts = df_merged['ev_count'].tolist()
  charger_counts = df_merged['charger_count'].tolist()

  # # 데이터 정의
  # regions = ['서울', '경기', '인천', '경상', '전라', '충청', '강원', '제주']
  # ev_counts = [83868, 151850, 54398, 80533, 56289, 56029, 21004, 49007]
  # charger_counts = [60615, 112384, 22349, 90573, 38585, 47247, 13818, 8561]

  # 위치 설정
  x = np.arange(len(regions))
  width = 0.35

  # 그래프 그리기
  fig, ax1 = plt.subplots(figsize=(12, 6))

  # 왼쪽 y축 - 전기차 등록 대수
  bar1 = ax1.bar(x - width/2, ev_counts, width, label='전기차 등록 대수', color='skyblue')
  ax1.set_xlabel('지역')
  ax1.set_ylabel('전기차 등록 대수', color='skyblue')
  ax1.tick_params(axis='y', labelcolor='skyblue')

  # 오른쪽 y축 - 충전기 개수
  ax2 = ax1.twinx()
  bar2 = ax2.bar(x + width/2, charger_counts, width, label='충전기 개수', color='orange')
  ax2.set_ylabel('충전기 개수', color='orange')
  ax2.tick_params(axis='y', labelcolor='orange')

  # x축 설정
  ax1.set_xticks(x)
  ax1.set_xticklabels(regions)

  # 제목 및 범례
  plt.title('지역별 전기차 등록 대수 및 충전기 개수 비교')
  fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

  # Streamlit에 그래프 출력
  st.pyplot(fig)
